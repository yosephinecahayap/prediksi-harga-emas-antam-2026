import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_pills import pills

st.set_page_config(
    page_title="Prediksi Harga Emas Antam",
    layout="wide"
)

st.markdown("""
<style>

.custom-info {
    background: rgba(0, 200, 255, 0.10);
    border: 1px solid rgba(0, 200, 255, 0.28);
    padding: 16px;
    border-radius: 14px;
}

.custom-warning {
    background: rgba(255, 184, 77, 0.12);
    border: 1px solid rgba(255, 184, 77, 0.28);
    padding: 16px;
    border-radius: 14px;
}

.custom-success {
    background: rgba(0, 220, 140, 0.10);
    border: 1px solid rgba(0, 220, 140, 0.30);
    padding: 16px;
    border-radius: 14px;
}

.big-text {
    font-size: 17px;
    line-height: 1.5;
    text-align: justify;
}

</style>
""", unsafe_allow_html=True)

# LOAD DATA

@st.cache_data
def load_data():

    emas = pd.read_csv("data/antam_price.csv")
    usd = pd.read_csv("data/kurs.csv")
    world = pd.read_csv("data/gold_idr.csv")
    pred = pd.read_csv("data/forecast.csv")

    for df in [emas, usd, world]:

        df.columns = df.columns.str.strip()

        if 'Tanggal' in df.columns:

            df['Tanggal'] = pd.to_datetime(
                df['Tanggal'],
                errors='coerce'
            )

            df.dropna(
                subset=['Tanggal'],
                inplace=True
            )

            df.drop_duplicates(
                subset=['Tanggal'],
                inplace=True
            )

    pred.columns = pred.columns.str.strip()

    if 'Forecast_Antam' in pred.columns:

        pred.rename(
            columns={'Forecast_Antam': 'prediksi'},
            inplace=True
        )

    if 'Harga' in emas.columns:

        emas.rename(
            columns={'Harga': 'harga'},
            inplace=True
        )

    if 'USD_IDR' in usd.columns:

        usd.rename(
            columns={'USD_IDR': 'kurs'},
            inplace=True
        )

    if 'Gold_IDR' in world.columns:

        world.rename(
            columns={'Gold_IDR': 'harga'},
            inplace=True
        )

    return emas, usd, world, pred


emas, usd, world, pred = load_data()

last_date = emas['Tanggal'].max()

pred['Tanggal'] = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=len(pred),
    freq='D'
)

# FORMAT RUPIAH

def format_rupiah(x):

    if x >= 1_000_000:

        val = x / 1_000_000

        return f'{val:g} Jt'

    elif x >= 1_000:

        val = x / 1_000

        return f'{val:g} Rb'

    else:

        return str(int(x))

def generate_insight(data):

    awal = data['prediksi'].iloc[0]
    akhir = data['prediksi'].iloc[-1]

    if akhir > awal:
        return "Naik"

    elif akhir < awal:
        return "Turun"

    else:
        return "Stabil"
            
# NAVBAR

selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Prediksi"],
    icons=["house-fill", "graph-up-arrow"],
    default_index=0,
    orientation="horizontal",

    styles={

        "container": {
            "padding": "0!important",
            "background-color": "transparent",
            "border-radius": "12px",
            "margin-bottom": "25px",
        },

        "icon": {
            "color": "inherit",
            "font-size": "18px"
        },

        "nav-link": {
            "font-size": "16px",
            "font-weight": "600",
            "text-align": "center",
            "margin": "0px",
            "padding": "12px",
            "border-radius": "10px",
            "color": "inherit",
            "--hover-color": "rgba(166,27,41,0.15)",
            "transition": "all 0.3s ease",
        },

        "nav-link-selected": {
            "background-color": "#A61B29",
            "color": "white",
            "font-weight": "700",
        },
    }
)

menu = selected

# DASHBOARD

if menu == "Dashboard":

    st.title("Dashboard Harga Emas Antam")

    st.subheader("Tentang Website")
    st.markdown("""
    <div class="big-text">

    Website ini merupakan sistem prediksi harga emas Antam yang dirancang untuk membantu pengguna memperoleh estimasi harga emas Antam hingga 90 hari ke depan. Prediksi dilakukan menggunakan data historis harga emas Antam, harga emas dunia, dan nilai tukar USD terhadap Rupiah (USD/IDR). Harga emas dunia dan nilai tukar USD/IDR digunakan karena keduanya merupakan faktor yang memengaruhi pergerakan harga emas Antam.

    Melalui website ini, pengguna dapat melihat informasi historis harga emas Antam, tren harga emas dunia, tren nilai tukar USD/IDR, serta hasil prediksi harga emas Antam untuk periode mendatang. Informasi yang disajikan diharapkan dapat membantu pengguna dalam memantau pergerakan harga emas dan menjadi referensi dalam pengambilan keputusan terkait investasi emas.

    Hasil prediksi yang ditampilkan merupakan estimasi berdasarkan data historis sehingga tidak dapat dijadikan jaminan terhadap harga aktual di masa mendatang.

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Petunjuk Penggunaan")

    st.markdown("""
    <div class="big-text">
        1. Buka halaman Dashboard untuk melihat informasi harga emas Antam, nilai tukar USD/IDR, dan harga emas dunia beserta grafik pergerakannya.<br>
        2. Pilih halaman Prediksi untuk mengakses fitur prediksi harga emas Antam.<br>
        3. Pilih tanggal prediksi yang tersedia pada kolom tanggal sesuai periode yang ingin dilihat.<br>
        4. Perhatikan nilai Harga Prediksi yang menampilkan estimasi harga emas Antam pada tanggal yang dipilih.<br>
        5. Perhatikan Tabel Prediksi Harga Emas Antam untuk mengetahui estimasi harga selama 7 hari berturut-turut mulai dari tanggal yang dipilih.<br>
        6. Perhatikan bagian Insight untuk mengetahui kecenderungan tren harga emas Antam pada periode 7 hari tersebut, apakah diprediksi naik, turun, atau stabil.<br>
        7. Gunakan pilihan periode grafik (1 Week, 1 Month, 2 Months, atau 3 Months) untuk menampilkan prediksi harga emas Antam sesuai rentang waktu yang diinginkan.<br>
        8. Amati grafik prediksi untuk melihat perkiraan pergerakan harga emas Antam pada periode yang dipilih.
    </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader(
        f"Tanggal terakhir data: {last_date.date()}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Emas Antam (per gram)",
        f"Rp {emas['harga'].iloc[-1]:,.0f}"
    )

    col2.metric(
        "USD/IDR",
        f"{usd['kurs'].iloc[-1]:,.0f}"
    )

    col3.metric(
        "Emas Dunia (per gram)",
        f"Rp {world['harga'].iloc[-1]:,.0f}"
    )

    st.subheader("Grafik Pergerakan Data")

    colA, colB, colC = st.columns(3)

    # GRAFIK EMAS ANTAM

    with colA:

        fig1 = go.Figure()

        fig1.add_trace(
            go.Scatter(
                x=emas['Tanggal'],
                y=emas['harga'],
                mode='lines',
                name='Emas Antam',
                line=dict(color='#00C2FF', width=3)
            )
        )

        fig1.update_layout(
            title="Emas Antam",
            height=400
        )

        tick_emas = [
            500000,
            1000000,
            2000000,
            3000000
        ]

        fig1.update_yaxes(
            tickvals=tick_emas,
            ticktext=[
                format_rupiah(x)
                for x in tick_emas
            ]
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # GRAFIK USD

    with colB:

        fig2 = go.Figure()

        fig2.add_trace(
            go.Scatter(
                x=usd['Tanggal'],
                y=usd['kurs'],
                mode='lines',
                name='USD/IDR',
                line=dict(color='#00C2FF', width=3)
            )
        )

        fig2.update_layout(
            title="USD/IDR",
            height=400
        )

        tick_usd = [
            5000,
            10000,
            15000,
            20000
        ]

        fig2.update_yaxes(
            tickvals=tick_usd,
            ticktext=[
                format_rupiah(x)
                for x in tick_usd
            ]
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # GRAFIK EMAS DUNIA

    with colC:

        fig3 = go.Figure()

        fig3.add_trace(
            go.Scatter(
                x=world['Tanggal'],
                y=world['harga'],
                mode='lines',
                name='Emas Dunia',
                line=dict(color='#00C2FF', width=3)
            )
        )

        fig3.update_layout(
            title="Emas Dunia",
            height=400
        )

        tick_world = [
            500000,
            1000000,
            2000000,
            3000000
        ]

        fig3.update_yaxes(
            tickvals=tick_world,
            ticktext=[
                format_rupiah(x)
                for x in tick_world
            ]
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

# PREDIKSI

elif menu == "Prediksi":

    st.title("Prediksi Harga Emas Antam")

    st.subheader("Pilih Tanggal Prediksi")

    min_tanggal = pred['Tanggal'].min()
    max_tanggal = pred['Tanggal'].max()

    selected_date = st.date_input(
        "Tanggal",
        value=min_tanggal,
        min_value=min_tanggal,
        max_value=max_tanggal
    )

    selected_data = pred[
        pred['Tanggal'] == pd.to_datetime(selected_date)
    ]


    if not selected_data.empty:

        harga = selected_data['prediksi'].values[0]

        st.metric(
            "Harga Prediksi",
            f"Rp {harga:,.0f}"
        )

    else:

        st.warning(
            "Tanggal tidak tersedia dalam data prediksi"
        )

    st.subheader("Tabel Prediksi Harga Emas Antam")

    table_idx = pred[
        pred['Tanggal'] == pd.to_datetime(selected_date)
    ].index

    if len(table_idx) > 0:

        table_idx = table_idx[0]

        tabel_7_hari = pred.iloc[
            table_idx : table_idx + 7
        ].copy()

        tabel_prediksi = tabel_7_hari[
            ['Tanggal', 'prediksi']
        ].copy()

        tabel_prediksi.columns = [
            "Tanggal",
            "Harga Prediksi"
        ]

        tabel_prediksi["Tanggal"] = (
            tabel_prediksi["Tanggal"]
            .dt.strftime("%d-%m-%Y")
        )

        tabel_prediksi["Harga Prediksi"] = (
            tabel_prediksi["Harga Prediksi"]
            .apply(lambda x: f"Rp {x:,.0f}")
        )

        st.dataframe(
            tabel_prediksi,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Insight")

        trend = generate_insight(
            tabel_7_hari
        )

        tanggal_akhir = tabel_7_hari[
            'Tanggal'
        ].iloc[-1]

        st.markdown(
            f"""
            <div class="custom-info">
                Tren harga emas Antam pada periode
                {selected_date.strftime('%d-%m-%Y')}
                hingga
                {tanggal_akhir.strftime('%d-%m-%Y')}
                diprediksi {trend}.
            </div>
            """,
            unsafe_allow_html=True
        )


    st.subheader(
        "Grafik Prediksi Beberapa Hari ke Depan"
    )

    periode = st.segmented_control(
        "Periode",
        ["1 Week", "1 Month", "2 Months", "3 Months"],
        default="1 Week"
    )

    hari_map = {
        "1 Week": 7,
        "1 Month": 30,
        "2 Months": 60,
        "3 Months": 90
    }

    hari = hari_map[periode]

    future = pred.head(hari)

    warna = '#00E5FF'

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=future['Tanggal'],
            y=future['prediksi'],
            mode='lines+markers',
            line=dict(
                color=warna,
                width=3
            ),
            marker=dict(
                size=7
            ),
            hovertemplate=
            "<b>Tanggal:</b> %{x}<br>" +
            "<b>Harga:</b> Rp %{y:,.0f}<extra></extra>"
        )
    )

    fig.update_layout(
        title=f"Prediksi {hari} Hari",
        xaxis_title="Tanggal",
        yaxis_title="Harga Prediksi",
        hovermode="x unified",
        height=450
    )

    fig.update_layout(
        yaxis=dict(
            tickformat=","
        )
    )

    if hari <= 7:
        nticks_val = hari

    elif hari <= 14:
        nticks_val = 7

    elif hari <= 30:
        nticks_val = 10

    elif hari <= 60:
        nticks_val = 8

    else:
        nticks_val = 6

    fig.update_xaxes(
        tickformat="%d %b",
        nticks=nticks_val,
        tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )