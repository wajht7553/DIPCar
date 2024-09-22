import re
import seaborn as sns
import matplotlib.pyplot as plt

# Function to extract mean IoU and accuracy from a log file


def extract_segmentation_metrics(log_file_path):
    iou_list = []
    accuracy_list = []

    with open(log_file_path, 'r') as f:
        for line in f:
            # Search for lines that contain the mean IoU and accuracy
            match = re.search(
                r'\(([\d.]+)% mean IoU, ([\d.]+)% accuracy\)', line)
            if match:
                mean_iou = float(match.group(1))  # Extract the IoU
                accuracy = float(match.group(2))  # Extract the accuracy
                iou_list.append(mean_iou)
                accuracy_list.append(accuracy)

    return iou_list, accuracy_list


# Assuming log file is 'segmentation_log.txt'
log_file_path = 'logs/fcn_train.txt'
mean_iou, accuracy = extract_segmentation_metrics(log_file_path)

sns.set_theme()
sns.set_style('whitegrid')
# Assuming the lists `mean_iou` and `accuracy` are already filled with data
epochs = list(range(1, len(mean_iou) + 1))  # Epoch numbers start from 1

# Set up a Seaborn style for better visualization
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))

# Plot Mean IoU over Epochs
plt.plot(epochs, mean_iou, label='Mean IoU',
         color='blue', marker='o', linewidth=2)

# Plot Accuracy over Epochs
plt.plot(epochs, accuracy, label='Accuracy',
         color='green', marker='x', linewidth=2)

# Customize plot with labels, title, and legend
plt.title('Mean IoU and Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Percentage')
plt.legend(loc='lower right')
plt.grid(True)

plt.suptitle('Fine-Tuning FCN-ResNet18')

# Save the plot as a high-quality image for inclusion in thesis
plt.savefig('segmentation_metrics_plot.png', dpi=600)

# Display the plot
plt.show()
