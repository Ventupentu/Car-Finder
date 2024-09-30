from dataset_loader import cargar_coches
from user_input import capturar_preferencias_usuario
from recommendation_engine import recomendar_coches

def main():
    # Cargar los coches del dataset
    coches = cargar_coches("data/coches.csv")

    # Capturar las preferencias del usuario
    preferencias_usuario = capturar_preferencias_usuario()

    # Realizar las recomendaciones basadas en las preferencias
    coches_recomendados = recomendar_coches(coches, preferencias_usuario)

    # Mostrar los coches recomendados
    print("\nCoches recomendados:")
    for coche in coches_recomendados:
        print(coche)

if __name__ == "__main__":
    main()
