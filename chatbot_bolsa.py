import yfinance as yf
import pandas as pd
import streamlit as st
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD

def descargar_datos(ticker):
    import yfinance as yf
    df = yf.download(ticker, start="2020-01-01", progress=False)
    
    # Revisar si se descargó algo
    if df.empty:
        raise ValueError(f"No se encontraron datos para el ticker '{ticker}'. Revisa que esté escrito correctamente.")
    
    # Corregir nombre de columna 'Adj Close' si es necesario
    if 'Adj. Close' in df.columns:
        df.rename(columns={'Adj. Close':'Adj Close'}, inplace=True)
    
    columnas_necesarias = ['Open','High','Low','Close','Adj Close','Volume']
    for col in columnas_necesarias:
        if col not in df.columns:
            raise KeyError(f"La columna '{col}' no existe en los datos descargados.")
    
    df = df[columnas_necesarias].dropna()
    return df


def agregar_indicadores(df):
    df = df.copy()
    df['sma_10'] = SMAIndicator(df['Adj Close'], window=10).sma_indicator()
    df['sma_50'] = SMAIndicator(df['Adj Close'], window=50).sma_indicator()
    df['rsi_14'] = RSIIndicator(df['Adj Close'], window=14).rsi()
    df['momentum_10'] = df['Adj Close'] - df['Adj Close'].shift(10)
    macd = MACD(df['Adj Close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df = df.dropna()
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
