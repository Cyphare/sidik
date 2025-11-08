import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

def train_interpretable_model(data_path):
    """
    Fungsi lengkap untuk melatih model Random Forest dan mengekstrak
    feature importance untuk pembuat kebijakan.
    """
    
    print(f"Memuat data dari {data_path}...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: File {data_path} tidak ditemukan.")
        return

    print("Melakukan pre-processing (one-hot encoding)...")
    df_processed = pd.get_dummies(df, columns=['pendidikan_kepala_keluarga', 'pekerjaan'])
    
    df_processed = df_processed.drop('id_keluarga', axis=1)

    y = df_processed['status_rentan']
    
    X = df_processed.drop('status_rentan', axis=1)
  
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Data dibagi: {len(X_train)} baris untuk latih, {len(X_test)} baris untuk uji.")
  
    print("Melatih model RandomForestClassifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, oob_score=True)
    
    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("\n--- HASIL EVALUASI MODEL ---")
    print(f"Akurasi Model: {accuracy * 100:.2f}%")

    print("\n--- INTERPRETASI MODEL (FEATURE IMPORTANCE) ---")
    print("Faktor-faktor apa yang paling penting untuk memprediksi 'status_rentan'?\n")
    
    importances = rf_model.feature_importances_
    feature_names = X.columns
    
    feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)

    print(feat_imp)

    plt.figure(figsize=(12, 8))
    sns.barplot(x=feat_imp.values, y=feat_imp.index, palette='viridis')
    plt.title('Faktor Paling Berpengaruh dalam Memprediksi Kerentanan', fontsize=16)
    plt.xlabel('Tingkat Kepentingan (Importance Score)', fontsize=12)
    plt.ylabel('Faktor Data (Fitur)', fontsize=12)
    plt.tight_layout()
    
    output_image = 'feature_importance_plot.png'
    plt.savefig(output_image)
    print(f"\nVisualisasi 'feature importance' disimpan sebagai {output_image}")

if __name__ == "__main__":
    train_interpretable_model('data_sdi_dummy.csv')
