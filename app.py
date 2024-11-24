from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from roboflow import Roboflow
import os
import svgwrite
from PIL import Image, ImageDraw
import json
import time
import uuid  # For generating unique filenames

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Roboflow API key and model details
API_KEY = "isOTd4zpX7uryn25kT9I"  # Replace with your actual API key
MODEL_ENDPOINT = "hands-suyu5"     # Replace with your actual model endpoint name
VERSION = 1                        # Replace with your model version

# Initialize Roboflow
rf = Roboflow(api_key=API_KEY)
project = rf.workspace().project(MODEL_ENDPOINT)
model = project.version(VERSION).model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save the uploaded file
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)  # Ensure the upload directory exists
    file.save(file_path)

    # Set session flag for processing
    session['processing'] = True
    session['file_path'] = file_path  # Store file path in session
    
    # Redirect to process page
    return redirect(url_for('process'))

@app.route('/process')
def process():
    # Render the process page, which will initiate the background processing
    return render_template('process.html')

@app.route('/start-process', methods=['POST'])
def start_process():
    file_path = session.get('file_path', None)
    if not file_path:
        return jsonify({"error": "File path not found"}), 400

    try:
        # Run inference
        result = model.predict(file_path).json()
        print("Inference result:", result)

        # Save the result to a JSON file instead of session
        result_id = str(uuid.uuid4())
        result_file = f"results/{result_id}.json"
        os.makedirs("results", exist_ok=True)
        with open(result_file, "w") as f:
            json.dump(result, f)

        # Store the result file path in session
        session['result_file'] = result_file

        # Save segmentations to PNG and SVG
        save_png_with_segmentations(file_path, result)
        save_svg_with_segmentations(result)

        # Clean up uploaded file after inference
        os.remove(file_path)

        # Return JSON with the redirect URL
        return jsonify({"redirect": url_for('results')})
    except Exception as e:
        print("Error during processing:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/results')
def results():
    # Fetch the result file path from the session
    result_file = session.get('result_file', None)
    if not result_file or not os.path.exists(result_file):
        return "No result data available.", 400

    # Load the result from the file
    with open(result_file, "r") as f:
        result = json.load(f)

    # Define paths for PNG and SVG
    png_path = "static/output_with_segmentation.png"
    svg_path = "static/output_with_segmentation.svg"

    return render_template('results.html', result=result, png_path=png_path, svg_path=svg_path)

def bezier_smooth(points, smooth_factor=0.7):
    # Smooths a list of points by converting them into a Bézier curve
    smoothed_points = []
    for i in range(len(points)):
        prev_point = points[i - 1]
        curr_point = points[i]
        next_point = points[(i + 1) % len(points)]

        control_point1 = (
            curr_point[0] * (1 - smooth_factor) + prev_point[0] * smooth_factor,
            curr_point[1] * (1 - smooth_factor) + prev_point[1] * smooth_factor
        )
        control_point2 = (
            curr_point[0] * (1 - smooth_factor) + next_point[0] * smooth_factor,
            curr_point[1] * (1 - smooth_factor) + next_point[1] * smooth_factor
        )

        smoothed_points.append(control_point1)
        smoothed_points.append(curr_point)
        smoothed_points.append(control_point2)

    return smoothed_points[::4]  # Adjust this number to reduce points further if needed

def save_png_with_segmentations(image_path, result):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        for pred in result['predictions']:
            points = [(p['x'], p['y']) for p in pred['points']]
            color = 'yellow' if pred['class'] == '0' else 'purple'  # Different colors for hand (0) and square (1)

            if pred['class'] == '0':  # Only smooth the hand outline
                points = bezier_smooth(points, smooth_factor=0.7)  # Higher smooth factor for extreme smoothness
                
            draw.line(points + [points[0]], fill=color, width=2, joint="curve")  # Rounded joints for smoothness
        
        os.makedirs("static", exist_ok=True)
        img.save("static/output_with_segmentation.png", "PNG")

def save_svg_with_segmentations(result):
    dwg = svgwrite.Drawing("static/output_with_segmentation.svg")
    for pred in result['predictions']:
        points = [(p['x'], p['y']) for p in pred['points']]
        color = "yellow" if pred['class'] == '0' else "purple"  # Different colors for hand (0) and square (1)
        
        if pred['class'] == '0':  # Only smooth the hand outline
            points = bezier_smooth(points, smooth_factor=0.7)
        
        polygon = dwg.polyline(points=points, stroke=color, fill="none", stroke_width=2)
        dwg.add(polygon)
    dwg.save()

if __name__ == '__main__':
    app.run(debug=True)
