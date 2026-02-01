import yfinance as yf
import pandas as pd
import streamlit as st
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD

import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD
import streamlit as st

def descargar_datos(ticker):
    # Descargar datos
    df = yf.download(ticker, start="2020-01-01", progress=False)
    
    if df.empty:
        st.error(f"No se encontraron datos para el ticker '{ticker}'. Revisa que esté escrito correctamente.")
        return None

    # Renombrar 'Adj. Close' si existe
    if 'Adj. Close' in df.columns:
        df.rename(columns={'Adj. Close':'Adj Close'}, inplace=True)
    
    # Comprobar columnas mínimas
    min_cols = ['Adj Close', 'Open', 'High', 'Low', 'Close', 'Volume']
    missing = [c for c in min_cols if c not in df.columns]
    if missing:
        st.warning(f"Algunas columnas faltan en los datos descargados: {missing}. Se usarán las disponibles.")
    
    return df

def agregar_indicadores(df):
    if df is None:
        return None
    
    df = df.copy()
    # Solo agregar indicadores si existen las columnas necesarias
    if 'Adj Close' in df.columns:
        df['sma_10'] = SMAIndicator(df['Adj Close'], window=10).sma_indicator()
        df['sma_50'] = SMAIndicator(df['Adj Close'], window=50).sma_indicator()
        df['rsi_14'] = RSIIndicator(df['Adj Close'], window=14).rsi()
        df['momentum_10'] = df['Adj Close'] - df['Adj Close'].shift(10)
        macd = MACD(df['Adj Close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
    else:
        st.warning("No se puede calcular indicadores porque 'Adj Close' no está disponible.")
    
    df.dropna(inplace=True)
    return df


def analizar_tendencia(df):
    ultima = df.iloc[-1]
    if ultima['sma_10'] > ultima['sma_50']:
        tendencia = "Alcista 📈"
    else:
        tendencia = "Bajista 📉"
    return tendencia

def recomendaciones_educativas(df):
    ultima = df.iloc[-1]
    if ultima['rsi_14'] < 70:
        return "Mantener o investigar para inversión a mediano plazo."
    else:
        return "Precaución: posible sobrecompra."

st.title("💹 Chatbot de Bolsa")
ticker = st.text_input("Escribe un ticker (AAPL, TSLA, MSFT)")

if ticker:
    df = agregar_indicadores(descargar_datos(ticker))
    st.write(analizar_tendencia(df))
    st.write(recomendaciones_educativas(df))
    st.line_chart(df[['Adj Close','sma_10','sma_50']])
