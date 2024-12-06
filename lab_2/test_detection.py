import cv2
import os
import time
import matplotlib.pyplot as plt
from detection import template_method, sift_method

image_path = "src/dogCat.jpg"
transformed_images_dir = "transformed_images"
results_dir = "matching_results"
graphs_dir = "matching_graphs"  # New directory for graphs

image = cv2.imread(image_path)
if image is None:
    print(f"Error: Could not load image '{image_path}'")
    exit()

if not os.path.exists(results_dir):
    os.makedirs(results_dir)

if not os.path.exists(graphs_dir):  # Create graphs directory
    os.makedirs(graphs_dir)

template_times = []
sift_times = []
filenames = []

for filename in os.listdir(transformed_images_dir):
    if filename.endswith(".png"):
        template_path = os.path.join(transformed_images_dir, filename)
        try:
            template = cv2.imread(template_path)
            if template is None:
                print(f"Warning: Could not load template '{template_path}'. Skipping.")
                continue

            filenames.append(filename)

            start_time = time.time()
            matched_image_template = template_method(image.copy(), template)
            end_time = time.time()
            template_times.append(end_time - start_time)

            start_time = time.time()
            matched_image_sift = sift_method(image.copy(), template)
            end_time = time.time()
            sift_times.append(end_time - start_time)

            # Save results (optional)
            template_filename = os.path.splitext(filename)[0]
            cv2.imwrite(
                os.path.join(results_dir, f"{template_filename}_template.png"),
                matched_image_template,
            )
            cv2.imwrite(
                os.path.join(results_dir, f"{template_filename}_sift.png"),
                matched_image_sift,
            )

            print(f"Results for '{filename}' processed.")

        except Exception as e:
            print(f"Error processing '{template_path}': {e}")


# Plotting the results
width = 0.35
x = range(len(filenames))

fig, ax = plt.subplots()
rects1 = ax.bar(x, template_times, width, label="Template Matching")
rects2 = ax.bar([i + width for i in x], sift_times, width, label="SIFT Matching")

ax.set_ylabel("Time (seconds)")
ax.set_title("Template Matching vs. SIFT Matching Time")
ax.set_xticks([i + width / 2 for i in x])
ax.set_xticklabels(filenames, rotation=45, ha="right")
ax.legend()

fig.tight_layout()

# Save the graph to the graphs directory
graph_filename = os.path.join(graphs_dir, "matching_times.png")
plt.savefig(graph_filename)  # Save the figure
plt.show()

print(f"All results saved to '{results_dir}' and graph saved to '{graph_filename}'")
