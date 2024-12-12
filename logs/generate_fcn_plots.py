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


def extract_loss(log_file_path):
    loss_list = []
    epoch_losses = []
    with open(log_file_path, 'r') as f:
        for line in f:
            match = re.search(r'loss: ([\d.]+)', line)
            if match:
                loss = float(match.group(1))
                epoch_losses.append(loss)
                if len(epoch_losses) == 5:  # Assuming each epoch has 5 steps
                    avg_loss = sum(epoch_losses) / len(epoch_losses)
                    loss_list.append(avg_loss)
                    epoch_losses = []  # Reset for the next epoch
    return loss_list



log_file_path = 'logs/fcn_train.txt'
mean_iou, accuracy = extract_segmentation_metrics(log_file_path)
loss = extract_loss(log_file_path)

sns.set_theme()
sns.set_style('whitegrid')
epochs = list(range(1, len(mean_iou) + 1))

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# First subplot for mean IoU and accuracy
ax1.plot(epochs, mean_iou, label='Mean IoU', color='blue', linewidth=2)
ax1.plot(epochs, accuracy, label='Accuracy', color='green', linewidth=2)
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Percentage')
ax1.set_title('Mean IoU and Accuracy')
ax1.legend()
ax1.grid(True)

# Second subplot for loss
ax2.plot(epochs, loss, label='Loss', color='red', linewidth=2)
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.set_title('Loss')
ax2.legend()
ax2.grid(True)

plt.suptitle('Fine-Tuning FCN-ResNet34')

# Save the plot as a high-quality image for inclusion in thesis
plt.savefig('segmentation_metrics_plot.png', dpi=600)

# Display the plot
plt.show()


print(len(mean_iou))
