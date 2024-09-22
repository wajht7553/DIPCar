import re
import seaborn as sns
import matplotlib.pyplot as plt

# Regular expressions to extract information from the log file
train_loss_pattern = r"Epoch: (\d+), Training Loss: ([\d\.]+), Training Regression Loss ([\d\.]+), Training Classification Loss: ([\d\.]+)"
val_loss_pattern = r"Epoch: (\d+), Validation Loss: ([\d\.]+), Validation Regression Loss ([\d\.]+), Validation Classification Loss: ([\d\.]+)"

# Lists to store extracted values
epochs = []
training_losses = []
training_regression_losses = []
training_classification_losses = []
validation_losses = []
validation_regression_losses = []
validation_classification_losses = []

# Read the log file
with open('logs/ssd_train.txt', 'r') as file:
    for line in file:
        # Search for training loss information
        train_match = re.search(train_loss_pattern, line)
        if train_match:
            epoch = int(train_match.group(1))
            training_loss = float(train_match.group(2))
            training_regression_loss = float(train_match.group(3))
            training_classification_loss = float(train_match.group(4))

            epochs.append(epoch)
            training_losses.append(training_loss)
            training_regression_losses.append(training_regression_loss)
            training_classification_losses.append(training_classification_loss)

        # Search for validation loss information
        val_match = re.search(val_loss_pattern, line)
        if val_match:
            epoch = int(val_match.group(1))
            validation_loss = float(val_match.group(2))
            validation_regression_loss = float(val_match.group(3))
            validation_classification_loss = float(val_match.group(4))

            validation_losses.append(validation_loss)
            validation_regression_losses.append(validation_regression_loss)
            validation_classification_losses.append(
                validation_classification_loss)
            
# Print the extracted values
print("Epochs:", epochs)
print("Training Losses:", len(training_losses))
print("Training Regression Losses:", len(training_regression_losses))
print("Training Classification Losses:", len(training_classification_losses))
print("Validation Losses:", len(validation_losses))
print("Validation Regression Losses:", len(validation_regression_losses))
print("Validation Classification Losses:", len(validation_classification_losses))


# Plot the training and validation losses
sns.set_theme()
sns.set_style("whitegrid")
plt.figure(figsize=(12, 5))

# Plot 1: Overall Training and Validation Loss Curves
plt.subplot(1, 2, 1)
plt.plot(epochs, training_losses, label='Avg Training Loss',
         color='blue', linewidth=2)
plt.plot(epochs, validation_losses, label='Avg Validation Loss',
         color='orange', linestyle='--', linewidth=2)
plt.title('Average Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

# Plot 4: Combined Loss Curves for Training and Validation (Regression and Classification)
plt.subplot(1, 2, 2)
plt.plot(epochs, training_regression_losses,
         label='Training Regression Loss', color='green', linewidth=2)
plt.plot(epochs, validation_regression_losses,
         label='Validation Regression Loss', color='green', linestyle='--', linewidth=2)
plt.plot(epochs, training_classification_losses,
         label='Training Classification Loss', color='red', linewidth=2)
plt.plot(epochs, validation_classification_losses,
         label='Validation Classification Loss', color='red', linestyle='--', linewidth=2)
plt.title('Regression and Classification Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

# Adjust layout for better appearance
# plt.tight_layout()
plt.suptitle("Fine-Tuning SSD-MobileNet")

# Save the plot as a high-quality image for inclusion in thesis
plt.savefig('learning_curves.png', dpi=600)

# Show the plot
plt.show()
