import os
import matplotlib.pyplot as plt

def generate_image(number, width=800, height=800, font_size=400, font_color='black', output_folder="output_images"):
    fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)

    # Configurar ejes para que no muestren nada
    ax.set_axis_off()

    # Configurar el tamaño y posición del texto en el centro
    text_x = 0.5
    text_y = 0.5

    # Añadir el texto a los ejes con el color especificado
    ax.text(text_x, text_y, str(number), fontsize=font_size, ha='center', va='center', color=font_color)

    # Configurar el fondo como transparente
    ax.set_facecolor((0, 0, 0, 0))

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Guardar la imagen en el disco dentro de la carpeta especificada
    output_file = os.path.join(output_folder, f"{number}.png")
    plt.savefig(output_file, transparent=True)
    plt.close()

if __name__ == "__main__":
    # Especifica el rango de números y la carpeta de salida
    start_number = 0
    end_number = 24  # Cambia esto al número final que desees
    output_folder = "img"

    # Genera imágenes para cada número en el rango especificado
    for number in range(start_number, end_number + 1):
        generate_image(number, output_folder=output_folder)
