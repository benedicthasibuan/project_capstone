import streamlit as st
import pandas as pd
#data interaktif
import plotly.express as px
#visualisasi plot
import plotly.graph_objects as go
#format angka
from numerize import numerize
#korelasi Pearson dan tau Kendall
import matplotlib.pyplot as plt

# Set Page
st.set_page_config(layout='wide')

# Dataset Loading
data_kualitasUdara = pd.read_csv('finaldata_kualitasUdara.csv')

# Mengurutkan DataFrame berdasarkan kolom 'tanggal'
data_kualitasUdara['tanggal'] = pd.to_datetime(data_kualitasUdara['tanggal'])
data_kualitasUdara.sort_values(by='tanggal', inplace=True)

# Title

st.title('Benarkah Kualitas Udara Mempengaru Resiko Penyakit Pernapasan Menular Melalui Udara?')

st.markdown('***Polusi Udara*** Pra Pandemi/Pasca Pandemi meningkatkan dampak resiko terkena penyakit menular, namun apakah benar demikian?')

# Visualisasi dengan Streamlit
st.subheader('Distribusi Materi Partikel Faktor Polusi Udara (2018-2022)')
select_freq, chart_full = st.columns([1,4])

chosen_freq = ''
with select_freq:
    freq = st.selectbox('Frekuensi Periode Waktu', ('Minggu','Bulan','Tahun'))
    if freq == 'Minggu':
        chosen_freq = 'W'
    elif freq == 'Bulan':
        chosen_freq = 'M'
    else:
        chosen_freq = 'Y'

with chart_full:
    data_full = data_kualitasUdara[['tanggal','pm10','so2','co','no2','o3']].set_index('tanggal').resample(chosen_freq).sum()
    st.line_chart(data_full)

st.write('Pada awal 2020, ***puncak fluktuasi*** tertinggi ada pada partikel PM10, SO2 dan CO. Pada awal 2020, pandemi COVID-19 mulai merebak di Indonesia khususnya di Jakarta. Pembatasan mobilitas dan lockdown telah menyebabkan penurunan aktivitas ekonomi dan emisi polutan. Hal ini berkontribusi pada penurunan fluktuasi PM10, SO2, dan CO di tahun 2021 dan 2022.')

# Chart each Year
st.subheader('Distribusi Kategori Kualitas Udara tiap Tahun')
selected_year, chart_1, chart_2 = st.columns([1,2,2])

chosen_year = -1
with selected_year:
    year = st.select_slider('Tahun',options=['2018','2019','2020','2021','2022'])
    if year == '2018':
        chosen_year = 2018
    elif year == '2019':
        chosen_year = 2019
    elif year == '2020':
        chosen_year = 2020
    elif year == '2021':
        chosen_year = 2021
    else:
        chosen_year = 2022

data = data_kualitasUdara[['tanggal','pm10','so2','co','no2','o3','categori']].set_index('tanggal')
data = data[data.index.year == chosen_year]['categori'].value_counts()
chart_data = pd.DataFrame()
chart_data['Categories'] = data.index
chart_data['Jumlah Sampel'] = data.values

with chart_1:
    fig = px.bar(chart_data, x='Categories', y ='Jumlah Sampel', color='Jumlah Sampel')
    fig.update_layout( yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    st.caption('Distribusi Kategori Kualitas Udara pada Tahun '+ year)

with chart_2:
    labels = list(chart_data['Categories'])
    values = list(chart_data['Jumlah Sampel'])

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    fig.update_layout(annotations=[dict(text=str(chosen_year), x=0.5, y=0.5,font_size=20, showarrow=False)])
    st.plotly_chart(fig, use_container_width=True)
    

# Metrics
st.markdown('### Volume Partikel Udara')
met1, met2, met3, met4, met5, met6 = st.columns(6)
data_kualitasUdara_now = data_kualitasUdara[data_kualitasUdara['tanggal'].dt.year == chosen_year]
data_kualitasUdara_last = data_kualitasUdara[data_kualitasUdara['tanggal'].dt.year == chosen_year-1]


with met1:
    if chosen_year == 2018:
        percentage = 0
    else:
        percentage = (data_kualitasUdara_now['pm10'].sum() - data_kualitasUdara_last['pm10'].sum()) / data_kualitasUdara_last['pm10'].sum()

    st.metric(
        'PM10',
        numerize.numerize(data_kualitasUdara_now['pm10'].sum()),
        str(round(percentage*100,2)) + '%',
        'inverse'
    )

with met2:
    if chosen_year == 2018:
        percentage = 0
    else:
        percentage = (data_kualitasUdara_now['co'].sum() - data_kualitasUdara_last['co'].sum()) / data_kualitasUdara_last['co'].sum()

    st.metric(
        'CO',
        numerize.numerize(data_kualitasUdara_now['co'].sum()),
        str(round(percentage*100,2)) + '%',
        'inverse'
    )

with met3:
    if chosen_year == 2018:
        percentage = 0
    else:
        percentage = (data_kualitasUdara_now['no2'].sum() - data_kualitasUdara_last['no2'].sum()) / data_kualitasUdara_last['no2'].sum()

    st.metric(
        'NO2',
        numerize.numerize(data_kualitasUdara_now['no2'].sum()),
        str(round(percentage*100,2)) + '%',
        'inverse'
    )

with met4:
    if chosen_year == 2018:
        percentage = 0
    else:
        percentage = (data_kualitasUdara_now['o3'].sum() - data_kualitasUdara_last['o3'].sum()) / data_kualitasUdara_last['o3'].sum()

    st.metric(
        'O3',
        numerize.numerize(data_kualitasUdara_now['o3'].sum()),
        str(round(percentage*100,2)) + '%',
        'inverse'
    )

with met5:
    if chosen_year == 2018:
        percentage = 0
    else:
        percentage = (data_kualitasUdara_now['so2'].sum() - data_kualitasUdara_last['so2'].sum()) / data_kualitasUdara_last['so2'].sum()

    st.metric(
        'SO2',
        numerize.numerize(data_kualitasUdara_now['so2'].sum()),
        str(round(percentage*100,2)) + '%',
        'inverse'
    )

with met6:
    st.markdown('#### Tahun ' + str(chosen_year))

# Penjelasan
teks = """
Kenaikan fluktuasi partikel polusi udara tetap terjadi dari tahun 2018-2021. 
Namun pada tahun 2018-2020, terjadi peningkatan fluktuasi di tahun 2019 terkhusus pada partikel PM10 dan O3.
Di tahun tersebut konsentrasi dari partikel polusi udara mencapai tahap SANGAT TIDAK SEHAT. 
Pada tahun 2020-2022, kategori SANGAT TIDAK SEHAT perlahan menghilang menandakan selama masa pandemi, udara di daerah 
DKI Jakarta semakin baik dengan berkurangnya polutan di udara.
"""

st.markdown(teks)

# Penderita Penyakit Menular di Provinsi DKI Jakarta (2018 - 2022)

st.subheader('Sebaran Penderita Penyakit TBC, PNEUMONIA DAN DIFTERI di Jakarta (2018-2022)')

# Dataset Loading
data_penyakitDKI = pd.read_csv('finaldata_penyakitDKI.csv')

# Mengurutkan DataFrame berdasarkan kolom 'tanggal'
data_penyakitDKI['tahun'] = pd.to_datetime(data_penyakitDKI['tahun'])
data_penyakitDKI.sort_values(by='tahun', inplace=True)

# Filter data berdasarkan tahun 2018-2022
data_penyakit_selected_years = data_penyakitDKI[(data_penyakitDKI['tahun'] >= '2018-01-01') & (data_penyakitDKI['tahun'] <= '2022-12-31')]

# Membagi layar menjadi dua baris
graph_and_selection = st.columns(2)

# Di dalam baris pertama (graph_and_selection)
with graph_and_selection[0]:
    # Memilih visualisasi
    graph = st.selectbox('Visualisasi Data', options=['Box Plot', 'Bar Chart','Line Chart'])

# Di dalam baris kedua (graph_and_selection)
with graph_and_selection[1]:
    # Memilih wilayah dengan nilai default DKI Jakarta
    selected_wilayah = st.selectbox('Pilih Wilayah', data_penyakit_selected_years['wilayah'].unique(), index=data_penyakit_selected_years['wilayah'].unique().tolist().index('DKI Jakarta'))

# Membuat grafik sesuai pilihan
if graph == 'Box Plot':
    # Membuat Box Plot dengan px.box
    fig = px.box(data_penyakit_selected_years[data_penyakit_selected_years['wilayah'] == selected_wilayah],
                 x='tahun', y=data_penyakit_selected_years.columns[2:],
                 color_discrete_map={'TB': 'blue', 'Pneumonia': 'green', 'Difteri': 'red'})
    fig.update_layout(title=f'Penyebaran Penyakit di {selected_wilayah} (2018-2023)',
                     xaxis_title='Tahun',
                     yaxis_title='Jumlah Kasus',
                     hovermode='closest')
    st.plotly_chart(fig, use_container_width=True)
elif graph == 'Line Chart':
    # Membuat Line Chart dengan px.line
    fig_line = px.line(data_penyakit_selected_years, x='tahun', y=['TB', 'Difteri', 'Pneumonia'], color='wilayah',
                       title='Tren Kasus TB, Difteri, dan Pneumonia per Wilayah',
                       labels={'value': 'Jumlah Kasus', 'wilayah': 'Wilayah'})
    st.plotly_chart(fig_line, use_container_width=True)
else:
    # Membuat Bar Chart dengan px.bar
    fig = px.bar(data_penyakit_selected_years[data_penyakit_selected_years['wilayah'] == selected_wilayah],
                 x='tahun', y=data_penyakit_selected_years.columns[2:],
                 color_discrete_map={'TB': 'blue', 'Pneumonia': 'green', 'Difteri': 'red'}, barmode='group')
    fig.update_layout(title=f'Penyebaran Penyakit di {selected_wilayah} (2018-2023)',
                     xaxis_title='Tahun',
                     yaxis_title='Jumlah Kasus',
                     hovermode='closest')
    st.plotly_chart(fig, use_container_width=True)

# ringkasan visualisasi
teksPenyakit = """
Dari data kasus TBC, Pneumonia, dan Difteri di Jakarta (2018-2022) kemudian divisualisasikan menjadi 3 visualisasi
1. Bar Chart secara jelas menunjukkan perbandingan kasus dan tren tahunan. 
2. Line Chart menegaskan kembali penurunan kasus TBC dan Difteri serta fluktuasi Pneumonia dari Bar Chart. 
3. Box Plot menggambarkan distribusi kasus dengan TBC dan Difteri cenderung memiliki lebih banyak kasus rendah.
Sedangkan Pneumonia, meskipun tidak simetris, memiliki distribusi kasus yang lebih merata dan penyebaran yang lebih terkendali dibandingkan dengan TBC dan difteri.
"""
st.markdown(teksPenyakit)
st.write("Dari ketiga visualisasi menunjukkan tren menurun pada TBC dan Difteri, dengan penurunan paling mencolok pada tahun 2020-2021 (sekitar 20% dan 80%). Pneumonia tetap menjadi penyakit dengan kasus tertinggi, mencapai puncak pada tahun 2020.")


st.subheader('Apakah Polusi Mempengaruhi Jumlah Kasus TBC, Pneunomia dan Difteri?')


# Pra-pemrosesan data kualitas udara
data_kualitasUdara['tanggal'] = pd.to_datetime(data_kualitasUdara['tanggal'])
data_kualitasUdara.sort_values(by='tanggal', inplace=True)

# Resample data ke frekuensi tahunan dan hitung rata-rata nilai-nilai
data_kualitasUdara_tahunan = data_kualitasUdara[['tanggal', 'pm10', 'so2', 'co', 'no2', 'o3']].set_index('tanggal')
data_kualitasUdara_tahunan = data_kualitasUdara_tahunan.resample('Y').mean()

# Fungsi untuk membuat line chart kualitas udara
def create_air_quality_line_chart(data):
    # Plot data
    st.line_chart(data)

# Buat dan tampilkan line chart kualitas udara
st.subheader("Tren Kualitas Udara di DKI Jakarta (2018-2022)")
create_air_quality_line_chart(data_kualitasUdara_tahunan)

# Fungsi untuk membuat line chart kasus penyakit
def create_disease_cases_line_chart(data):
    fig_line_penyakit = px.line(data, x='tahun', y=['TB', 'Difteri', 'Pneumonia'],
                                title='Tren Kasus TB, Difteri, dan Pneumonia',
                                labels={'value': 'Jumlah Kasus', 'wilayah': 'Wilayah'})
    st.plotly_chart(fig_line_penyakit, use_container_width=True)

# Filter data untuk DKI Jakarta
data_penyakitDKI_Jakarta = data_penyakitDKI[data_penyakitDKI['wilayah'] == 'DKI Jakarta']

# Tentukan frekuensi yang dipilih untuk resampling data kualitas udara
chosen_freq = 'Y'  # Resample ke frekuensi tahunan


# Buat dan tampilkan line chart kasus penyakit
st.subheader("Tren Penyakit di DKI Jakarta (2018-2022)")
create_disease_cases_line_chart(data_penyakitDKI_Jakarta)

teks_analisa = """
Grafik pertama memberikan gambaran tentang fluktuasi tingkat PM10, O3, SO2, NO2, dan CO
selama awal tahun 2020. Faktor-faktor yang mungkin berkontribusi termasuk peningkatan aktivitas industri, 
kendaraan bermotor, kebakaran hutan, dan fenomena alam seperti El Niño. 
Menariknya, pada grafik kedua, terlihat tren penurunan kasus TBC, pneumonia, dan difteri di Jakarta selama tahun-tahun yang sama.
Penurunan kasus penyakit tersebut kemungkinan besar terkait dengan dampak pandemi COVID-19. 
Pembatasan mobilitas masyarakat, peningkatan protokol kesehatan, dan penurunan akses ke layanan kesehatan dapat menjadi faktor penyebab. 
Penurunan ini juga dipengaruhi oleh faktor-faktor lain seperti perubahan perilaku masyarakat bukan semata-mata
kalau polusi udaralah penyebabnya. Polusi udara membantu meningkatkan penyebaran penyakit ini melalui udara.
Bila dilihat melalu beberapa grafik korelasi antara tingkat polutan dan TBC menunjukkan hubungan positif, 
serta antara polutan dan pneumonia, mengindikasikan bahwa peningkatan polusi udara dapat meningkatkan risiko terkena penyakit pernapasan.
"""
st.markdown(teks_analisa)

st.subheader("Kesimpulan")
teks_kesimpulan = """
Hasil analisis saya selama polusi udara, terutama PM10, PM2.5, dan NO2 
dapat meningkatkan risiko penyakit pernapasan seperti TBC dan pneumonia. Dikarenakan kedua partikel ini dapat 
masuk ke paru-paru dan menyebabkan peradangan. Dilihat dari beberapa grafik, pada masa pra pandemi tingkat polusi
udara sangat tinggi dan mencapai kategori SANGAT TIDAK SEHAT. Berbanding saat mulai pandemi, tingkat polusi berkurang dan kemudian meningkat kembali
segera setelah lockdown tidak diberlakukan yaitu mulai 2021 dan adanya  Pemberlakuan Pembatasan Kegiatan Masyarakat (PPKM) berbasis mikro dijalankan pada bulan Februari 2021.
Hal ini juga selaras dengan meningkatnya kasus penyakit menular seperti TB dan Pneumonia di awal tahun 2021.
"""
st.markdown(teks_kesimpulan)

# Menampilkan footnote dengan tautan yang dapat diklik
st.markdown("Sumber data: [Open Data](https://data.go.id/home), [Satu Data Jakarta](https://satudata.jakarta.go.id/home)")