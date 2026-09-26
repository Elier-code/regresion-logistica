import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Variables globales para guardar el modelo y saber si ya se cargaron los datos
df = None
modelo = None

def cargar():
    global df, modelo
    ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])

    if ruta == "":
        return

    try:
        df = pd.read_csv(ruta)
        
        # Separar variables de entrada (X) y variable objetivo (y)
        X = df[["precio", "descuento", "visitas", "calificacion"]]
        y = df["comprado"]

        # Separar datos en 80% para entrenar y 20% para pruebas
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Crear y entrenar la regresion logistica
        modelo = LogisticRegression()
        modelo.fit(X_train, y_train)

        # Evaluar el modelo con el conjunto de prueba (20%)
        y_pred = modelo.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

        # Mostrar que el archivo se cargó con éxito
        etiqueta_archivo.config(text="Archivo cargado correctamente", fg="green")

        # Mostrar los resultados de las métricas en pantalla
        texto_evaluacion = (
            f"Accuracy: {acc*100:.1f}%\n"
            f"Precision: {prec*100:.1f}%\n"
            f"Recall: {rec*100:.1f}%\n"
            f"F1-Score: {f1*100:.1f}%\n"
            f"Matriz de Confusión:\n"
            f"VN: {cm[0][0]} | FP: {cm[0][1]}\n"
            f"FN: {cm[1][0]} | VP: {cm[1][1]}"
        )
        etiqueta_metricas.config(text=texto_evaluacion)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")

def predecir():
    if modelo is None:
        messagebox.showwarning("Aviso", "Primero carga el archivo CSV para entrenar el modelo")
        return

    try:
        # Obtener los datos de los campos de texto
        precio = float(caja1.get())
        descuento = float(caja2.get())
        visitas = float(caja3.get())
        calificacion = float(caja4.get())
    except ValueError:
        messagebox.showerror("Error", "Ingresa números válidos en todos los campos")
        return

    # Realizar la predicción
    datos_nuevos = [[precio, descuento, visitas, calificacion]]
    resultado = modelo.predict(datos_nuevos)
    prob = modelo.predict_proba(datos_nuevos)

    # Mostrar resultado y probabilidad en la interfaz
    if resultado[0] == 1:
        texto = f"Resultado: SÍ se comprará\nProbabilidad: {prob[0][1]*100:.1f}%"
        etiqueta_resultado.config(text=texto, fg="green")
    else:
        texto = f"Resultado: NO se comprará\nProbabilidad: {prob[0][1]*100:.1f}%"
        etiqueta_resultado.config(text=texto, fg="red")


# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Productech - Predicción de Compras")
ventana.config(bg="#f0f4f8", padx=50, pady=50)

# Título Principal
titulo = tk.Label(ventana, text="Logística simple", font=("Arial", 13, "bold"), bg="#f0f4f8", fg="#102a43")
titulo.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

# --- Sección 1: Carga y Evaluación ---
boton_cargar = tk.Button(ventana, text="1. Cargar CSV y Entrenar", command=cargar, bg="#2b6cb0", fg="white", font=("Arial", 10, "bold"), width=25)
boton_cargar.grid(row=1, column=0, columnspan=2, pady=5, padx=10)

etiqueta_archivo = tk.Label(ventana, text="Sin archivo cargado", font=("Arial", 9, "italic"), bg="#f0f4f8", fg="gray")
etiqueta_archivo.grid(row=2, column=0, columnspan=2, pady=2)

etiqueta_metricas = tk.Label(ventana, text="Evaluación del modelo: N/A", font=("Arial", 9), bg="#ffffff", relief="solid", bd=1, justify="left", padx=10, pady=5)
etiqueta_metricas.grid(row=3, column=0, columnspan=2, pady=8, padx=10)

# --- Sección 2: Entrada de datos ---
lbl_precio = tk.Label(ventana, text="Precio:", bg="#f0f4f8", font=("Arial", 9, "bold"))
lbl_precio.grid(row=4, column=0, sticky="e", padx=10, pady=4)
caja1 = tk.Entry(ventana)
caja1.grid(row=4, column=1, sticky="w", padx=10, pady=4)

lbl_descuento = tk.Label(ventana, text="Descuento:", bg="#f0f4f8", font=("Arial", 9, "bold"))
lbl_descuento.grid(row=5, column=0, sticky="e", padx=10, pady=4)
caja2 = tk.Entry(ventana)
caja2.grid(row=5, column=1, sticky="w", padx=10, pady=4)

lbl_visitas = tk.Label(ventana, text="Visitas:", bg="#f0f4f8", font=("Arial", 9, "bold"))
lbl_visitas.grid(row=6, column=0, sticky="e", padx=10, pady=4)
caja3 = tk.Entry(ventana)
caja3.grid(row=6, column=1, sticky="w", padx=10, pady=4)

lbl_calificacion = tk.Label(ventana, text="Calificación:", bg="#f0f4f8", font=("Arial", 9, "bold"))
lbl_calificacion.grid(row=7, column=0, sticky="e", padx=10, pady=4)
caja4 = tk.Entry(ventana)
caja4.grid(row=7, column=1, sticky="w", padx=10, pady=4)

# --- Sección 3: Botón de Predicción y Resultados ---
boton_predecir = tk.Button(ventana, text="2. Predecir", command=predecir, bg="#2f855a", fg="white", font=("Arial", 10, "bold"), width=25)
boton_predecir.grid(row=8, column=0, columnspan=2, pady=12, padx=10)

etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 11, "bold"), bg="#f0f4f8")
etiqueta_resultado.grid(row=9, column=0, columnspan=2, pady=5)

ventana.mainloop()