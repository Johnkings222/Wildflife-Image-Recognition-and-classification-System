"""
Wildlife Image Recognition System - Main Application
A Tkinter-based GUI for wildlife species recognition using Siamese Networks
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
import os
from siamese_network import WildlifeRecognitionModel


class WildlifeRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wildlife Image Recognition System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Initialize model (lazy loading)
        self.model = None
        self.current_image_path = None
        self.current_photo = None

        # Create UI
        self.create_widgets()

        # Status
        self.update_status("Ready")

    def create_widgets(self):
        """Create all UI components"""

        # Title Frame
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="Wildlife Image Recognition System",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)

        # Main container
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Top Frame - Buttons
        button_frame = tk.Frame(main_container, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # Upload Button
        self.upload_btn = tk.Button(
            button_frame,
            text="📁 Upload Image",
            command=self.upload_image,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3
        )
        self.upload_btn.pack(side=tk.LEFT, padx=5)

        # Clear Button
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑 Clear",
            command=self.clear_all,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Content Frame - Image and Predictions
        content_frame = tk.Frame(main_container, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left Frame - Image Display
        left_frame = tk.LabelFrame(
            content_frame,
            text="Uploaded Image",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
            bd=2,
            relief=tk.GROOVE
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Canvas for image
        self.canvas = tk.Canvas(
            left_frame,
            bg="#ecf0f1",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Placeholder text on canvas
        self.canvas_text = self.canvas.create_text(
            0, 0,
            text="No image uploaded\nClick 'Upload Image' to begin",
            font=("Arial", 14),
            fill="#95a5a6",
            justify=tk.CENTER
        )

        # Right Frame - Predictions
        right_frame = tk.LabelFrame(
            content_frame,
            text="Top Predictions",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
            bd=2,
            relief=tk.GROOVE,
            width=300
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 0))
        right_frame.pack_propagate(False)

        # Predictions container with scrollbar
        predictions_container = tk.Frame(right_frame, bg="white")
        predictions_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbar for predictions
        scrollbar = tk.Scrollbar(predictions_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget for predictions
        self.predictions_text = tk.Text(
            predictions_container,
            font=("Courier New", 11),
            bg="#ffffff",
            fg="#2c3e50",
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.predictions_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.predictions_text.yview)

        # Configure text tags for styling
        self.predictions_text.tag_configure("header", font=("Arial", 12, "bold"), foreground="#2c3e50")
        self.predictions_text.tag_configure("species", font=("Arial", 11, "bold"), foreground="#27ae60")
        self.predictions_text.tag_configure("confidence", font=("Courier New", 10), foreground="#7f8c8d")
        self.predictions_text.tag_configure("separator", foreground="#bdc3c7")

        # Bottom Frame - Status Bar
        status_frame = tk.Frame(self.root, bg="#34495e", height=35)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        # Bind canvas resize event
        self.canvas.bind("<Configure>", self.on_canvas_resize)

    def on_canvas_resize(self, event):
        """Handle canvas resize to update placeholder text or image"""
        # Update placeholder text position
        self.canvas.coords(self.canvas_text, event.width // 2, event.height // 2)

        # Redraw image if one is loaded
        if self.current_image_path and os.path.exists(self.current_image_path):
            self.display_image(self.current_image_path)

    def upload_image(self):
        """Handle image upload"""
        file_path = filedialog.askopenfilename(
            title="Select Wildlife Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tiff *.tif *.jfif *.JPG *.JPEG *.PNG *.BMP *.GIF *.WEBP *.TIFF *.TIF *.JFIF"),
                ("JPEG files", "*.jpg *.jpeg *.JPG *.JPEG *.jfif *.JFIF"),
                ("PNG files", "*.png *.PNG"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.predict_species(file_path)

    def display_image(self, image_path):
        """Display image on canvas with automatic resizing"""
        try:
            # Hide placeholder text
            self.canvas.itemconfig(self.canvas_text, state='hidden')

            # Open image
            image = Image.open(image_path)

            # Get canvas dimensions
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Calculate scaling to fit image in canvas while maintaining aspect ratio
            img_width, img_height = image.size
            scale_w = canvas_width / img_width
            scale_h = canvas_height / img_height
            scale = min(scale_w, scale_h) * 0.95  # 95% to leave some margin

            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            self.current_photo = ImageTk.PhotoImage(image)

            # Clear canvas and display image
            self.canvas.delete("image")
            self.canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=self.current_photo,
                anchor=tk.CENTER,
                tags="image"
            )

            self.update_status(f"Image loaded: {os.path.basename(image_path)}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
            self.update_status("Error loading image")

    def predict_species(self, image_path):
        """Predict species in a separate thread"""
        self.update_status("Predicting...")

        # Disable buttons during prediction
        self.upload_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)

        # Run prediction in separate thread to avoid freezing UI
        thread = threading.Thread(target=self._predict_worker, args=(image_path,))
        thread.daemon = True
        thread.start()

    def _predict_worker(self, image_path):
        """Worker thread for prediction"""
        try:
            # Initialize model if not already done
            if self.model is None:
                self.root.after(0, self.update_status, "Loading model...")
                self.model = WildlifeRecognitionModel()

            # Make prediction
            predictions = self.model.predict(image_path, top_k=5)

            # Update UI on main thread
            self.root.after(0, self.display_predictions, predictions)
            self.root.after(0, self.update_status, "Prediction complete!")

        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", f"Prediction failed:\n{str(e)}")
            self.root.after(0, self.update_status, "Prediction failed")

        finally:
            # Re-enable buttons
            self.root.after(0, lambda: self.upload_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.clear_btn.config(state=tk.NORMAL))

    def display_predictions(self, predictions):
        """Display prediction results"""
        # Enable text widget for editing
        self.predictions_text.config(state=tk.NORMAL)
        self.predictions_text.delete(1.0, tk.END)

        # Header
        self.predictions_text.insert(tk.END, "PREDICTION RESULTS\n", "header")
        self.predictions_text.insert(tk.END, "=" * 35 + "\n\n", "separator")

        # Top prediction (highlighted)
        if predictions:
            top_species, top_confidence = predictions[0]
            self.predictions_text.insert(tk.END, "Top Prediction:\n", "header")
            self.predictions_text.insert(tk.END, f"🦁 {top_species}\n", "species")
            self.predictions_text.insert(tk.END, f"Confidence: {top_confidence:.2f}%\n\n", "confidence")
            self.predictions_text.insert(tk.END, "-" * 35 + "\n\n", "separator")

        # All predictions
        self.predictions_text.insert(tk.END, "All Predictions:\n", "header")
        self.predictions_text.insert(tk.END, "-" * 35 + "\n", "separator")

        for i, (species, confidence) in enumerate(predictions, 1):
            # Rank emoji
            rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1] if i <= 5 else f"{i}."

            self.predictions_text.insert(tk.END, f"\n{rank_emoji} ", "confidence")
            self.predictions_text.insert(tk.END, f"{species}\n", "species")

            # Confidence bar
            bar_length = int(confidence / 5)  # Scale to 20 chars max
            bar = "█" * bar_length + "░" * (20 - bar_length)
            self.predictions_text.insert(tk.END, f"   {bar} {confidence:.2f}%\n", "confidence")

        # Disable text widget
        self.predictions_text.config(state=tk.DISABLED)

    def clear_all(self):
        """Clear all data and reset interface"""
        # Clear image
        self.canvas.delete("image")
        self.canvas.itemconfig(self.canvas_text, state='normal')
        self.current_image_path = None
        self.current_photo = None

        # Clear predictions
        self.predictions_text.config(state=tk.NORMAL)
        self.predictions_text.delete(1.0, tk.END)
        self.predictions_text.config(state=tk.DISABLED)

        # Reset status
        self.update_status("Ready")

    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = WildlifeRecognitionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
