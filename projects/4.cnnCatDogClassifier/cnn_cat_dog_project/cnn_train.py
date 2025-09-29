import os
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import seaborn as sns
from datetime import datetime
from sklearn.metrics import confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models, callbacks

# Timestamp for versioning
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Versioned Paths
base_path = '/tf/code/models'
model_save_path = f'{base_path}/cat_dog_cnn_model.h5'
acc_plot_path = f'{base_path}/accuracy_plot_{timestamp}.png'
conf_matrix_plot_path = f'{base_path}/confusion_matrix_{timestamp}.png'
log_file_path = f'{base_path}/training_log_{timestamp}.csv'

# Suppress all TF logs except warnings and errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

# Dataset Path
original_data_dir = '/tf/code/dataset/PetImages'

# Data generators with validation split
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    original_data_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='training',
    shuffle=True
)

val_generator = train_datagen.flow_from_directory(
    original_data_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='validation',
    shuffle=False
)

print("Class Indices:", train_generator.class_indices)

# CNN Model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),

    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # Binary classification
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# CSV Logger for saving epoch-wise metrics
csv_logger = callbacks.CSVLogger(log_file_path, append=False)

# Train the model
history = model.fit(
    train_generator,
    epochs=6,
    validation_data=val_generator,
    callbacks=[csv_logger],
    verbose=1
)

# Save the model
model.save(model_save_path)

# Save Accuracy Plot
plt.figure(figsize=(8, 6))
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title("Accuracy vs Epochs")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.savefig(acc_plot_path)
plt.close()

# Generate Confusion Matrix
val_generator.reset()
pred_probs = model.predict(val_generator, verbose=1)
pred_classes = (pred_probs > 0.5).astype("int32").flatten()
true_classes = val_generator.classes

conf_mat = confusion_matrix(true_classes, pred_classes)
plt.figure(figsize=(6, 5))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues',
            xticklabels=list(train_generator.class_indices.keys()),
            yticklabels=list(train_generator.class_indices.keys()))
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.savefig(conf_matrix_plot_path)
plt.close()

print(f"Model saved to: {model_save_path}")
print(f"Accuracy plot saved to: {acc_plot_path}")
print(f"Confusion matrix plot saved to: {conf_matrix_plot_path}")
print(f"Training log saved to: {log_file_path}")
