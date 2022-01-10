import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='WCS', page_icon=':red_car:')

st.markdown("<h1 style='text-align: center;'>Projet Wild Code School : Analyse des données des voitures</h1>", unsafe_allow_html=True)

def _max_width_():
    max_width_str = "max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

@st.cache
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv')

df_cars = load_data()

df_eu = df_cars[df_cars['continent'] == ' Europe.']
df_usa = df_cars[df_cars['continent'] == ' US.']
df_jp = df_cars[df_cars['continent'] == ' Japan.']

st.title('') 

def main():

    pages = {
        'Accueil': home,
        'Heatmaps de corrélation': heatmaps,
        'Distributions': histograms,
        'Nuages de points': scatters
        }

    if "page" not in st.session_state:
        st.session_state.update({
        # Default page
        'page': 'Accueil'
        })

    with st.sidebar:
        page = st.selectbox("Choisissez une page", tuple(pages.keys()))

    pages[page]()
    
def home():
    st.markdown("<h2 style = 'text-align : center'>A Propos</h2>", unsafe_allow_html=True)
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    
    "Ce projet a pour but de créer un dashboard à l'aide de Streamlit qui permet de visualiser des informations provenant d'un dataset recensant les caractéristiques de certaines voitures sorties entre 1971 et 1983, en fonction de leur région d'origine."
    
    "Vous pouvez utiliser le menu latéral pour choisir le type de visualisations que vous souhaitez voir."
    
    "A noter que toutes les données sont au format impérial et non métrique."
    
    'Vous pouvez voir ici un aperçu des données à étudier (vous pouvez utiliser la molette pour descendre dans le tableau, et cliquer sur une colonne pour trier en fonction) :\n\n'
    
    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.write('\n')
        st.dataframe(df_cars)
    
    st.write('\n')
    
    st.markdown('* mpg : consommation en miles par gallon (impérial)')
    st.markdown('* cylinders : nombre de cylindres de la voiture')
    st.markdown('* cubinches : cylindrée en cubic inches (122 cubic inches = 2 litres)')
    st.markdown('* hp : puissance en chevaux')
    st.markdown('* weightlbs : poids en livres (1 livre = 0.454 kg')
    st.markdown('* time-to-60 : temps pour aller de 0 à 60 miles par heure (presque équivalent au 0 à 100 kmh)')
    st.markdown('* year : année de sortie du modèle')
    st.markdown('* continent : région d\'origine de la voiture (entre Europe, USA et Japon)')

    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    
    
    'Créé par Guillaume Arp.'

def heatmaps():
    
    def draw_corr_heatmap(region):
     
        if region == 'Europe':
            df = df_eu
        elif region == 'USA':
            df = df_usa
        elif region =='Japon':
            df = df_jp
        else:
            df = df_cars

        corr = df.corr()

        fig = go.Figure()

        fig.add_trace(go.Heatmap(
            z = corr,
            x = corr.columns.values,
            y = corr.columns.values,
            colorscale=px.colors.diverging.RdBu,
            zmid=0
        ))

        fig.update_layout(width=650, height=650, title=f'Heatmap de corrélation pour {region}', template='plotly_dark')
        return fig
    
    'Vous pouvez ici afficher des heatmaps de correlation pour chaque région, ou pour les données globales, à l\'aide des menus déroulants.'
    
    col1, col2 = st.columns(2)
    
    with col1:
        region = st.selectbox('Sélectionnez une région', ('Europe', 'USA', 'Japon', 'Global'), key=1, index=3)
        st.plotly_chart(draw_corr_heatmap(region))
        
    with col2:
        region = st.selectbox('Sélectionnez une région', ('Europe', 'USA', 'Japon', 'Global'), key=2, index=0)
        st.plotly_chart(draw_corr_heatmap(region))
        
    'On peut noter que les corrélations sont beaucoup plus fortes pour les voitures américaines, notamment en ce qui concerne la consommation (exprimée ici en mpg : miles per gallon).'

def histograms():
    
    def draw_histogram(col, region, bins):
    
        if region == 'Europe':
            df = df_eu
            cmap = ['limegreen']
        elif region == 'USA':
            df = df_usa
            cmap = ['coral']
        elif region =='Japon':
            df = df_jp
            cmap = ['linen']
        else:
            df = df_cars
            cmap = ['darkviolet']
        
        fig = px.histogram(df, x=col, nbins=bins, title=f'Distribution de {col} pour {region}', color_discrete_sequence=cmap)
        fig.update_layout(width=650, height=500, template='plotly_dark')
        return fig
    
    'Vous pouvez ici afficher des histogrammes de la donnée dont vous voulez afficher la distribution, en choisissant les paramètres à l\'aide des sélecteurs.'
    
    cols = df_cars.columns.to_list()
    
    col11, col12, col13, col14, col15, col16, col17 = st.columns([3,3,3,1,3,3,3])
    
    with col11:
        region1 = st.selectbox('Sélectionnez une région', ('Europe', 'USA', 'Japon', 'Global'), key=1, index=3)
    
    with col12:
        column1 = st.selectbox('Sélectionnez une colonne', cols, key=2, index=1)
        
    with col13:
        nbins1 = st.slider("Nombre de bins", min_value=2, max_value=100, value=20, step=1, key=5)
        
    with col15:
        region2 = st.selectbox('Sélectionnez une région', ('Europe', 'USA', 'Japon', 'Global'), key=3, index=0)
    
    with col16:
        column2 = st.selectbox('Sélectionnez une colonne', cols, key=4, index=0)
        
    with col17:
        nbins2 = st.slider("Nombre de bins", min_value=2, max_value=100, value=20, step=1, key=6)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(draw_histogram(column1, region1, nbins1))
        
    with col2:
        st.plotly_chart(draw_histogram(column2, region2, nbins2))
        
    col11, col12, col13, col14, col15, col16, col17 = st.columns([3,3,3,1,3,3,3])
    
    with col11:
        region1 = st.selectbox('Sélectionnez une région', ('Europe', 'USA', 'Japon', 'Global'), key=11, index=1)
    
    with col12:
        column1 = st.selectbox('Sélectionnez une colonne', cols, key=12, index=2)
        
    with col13:
        nbins1 = st.slider("Nombre de bins", min_value=2, max_value=100, value=20, step=1, key=15)
        
    with col15:
        region2 = st.selectbox('Sélectionnez une région', ('Europe', 'USA', 'Japon', 'Global'), key=13, index=2)
    
    with col16:
        column2 = st.selectbox('Sélectionnez une colonne', cols, key=14, index=3)
        
    with col17:
        nbins2 = st.slider("Nombre de bins", min_value=2, max_value=100, value=20, step=11, key=16)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(draw_histogram(column1, region1, nbins1))
        
    with col2:
        st.plotly_chart(draw_histogram(column2, region2, nbins2))
        
    "De façon générale, on peut noter ici que les voitures américaines ont tendance à cette période à être beaucoup plus puissantes, et avec plus de cylindres, que les voitures européennes et japonaises en comparaison. On peut noter par exemple que le V8 est majoritaire aux USA, mais inexistant dans le reste du monde. Logiquement, la consommation est bien plus élevée aux USA, et l\'autonomie des véhicules s'en resset, avec un mode autour de 15 mpg pour les voitures américaines, contre 27 pour les européennes et 32 pour les japonaises."

def scatters():
    
    def draw_scatter(col1, col2, region):
        
        if region == 'Europe':
            df = df_eu
            cmap = ['limegreen']
        elif region == 'USA':
            df = df_usa
            cmap = ['coral']
        elif region =='Japon':
            df = df_jp
            cmap = ['linen']
        else:
            df = df_cars

        region_list = ['Europe', 'USA', 'Japon']
        
        if region not in region_list:
            fig = px.scatter(df, x=col1, y=col2, color='continent', color_discrete_sequence=['coral', 'limegreen', 'linen'], title=f'Nuage de points entre {col1} et {col2} au niveau mondial', opacity=0.7)
            fig.update_layout(width=650, height=500, template='plotly_dark')
            return fig
            
        else:
            fig = px.scatter(df, x=col1, y=col2, title=f'Nuage de points entre {col1} et {col2} pour {region}', color_discrete_sequence=cmap, opacity=0.8)
            fig.update_layout(width=650, height=500, template='plotly_dark')
            return fig
        
    cols = df_cars.columns.to_list()
        
    'Vous pouvez ici afficher des nuages de points entre deux colonnes au choix, et en filtrant également par région, à l\'aide des menus.'
    
    col11, col12, col13, col14, col15, col16, col17 = st.columns([3,3,3,1,3,3,3])
    
    with col11:
        region1 = st.selectbox('Sélectionnez une région', ('Europe', 'USA', 'Japon', 'Global'), key=21, index=3)
    
    with col12:
        col_scatter1 = st.selectbox('Sélectionnez l\'axe x', cols, key=22, index=0)
        
    with col13:
        col_scatter2 = st.selectbox('Sélectionnez l\'axe y', cols, key=25, index=1)
        
    with col15:
        region2 = st.selectbox('Sélectionnez une région', ('Europe', 'USA', 'Japon', 'Global'), key=23, index=0)
    
    with col16:
        col_scatter3 = st.selectbox('Sélectionnez l\'axe x', cols, key=24, index=2)
        
    with col17:
        col_scatter4 = st.selectbox('Sélectionnez l\'axe y', cols, key=26, index=3)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(draw_scatter(col_scatter1, col_scatter2, region1))
        
    with col2:
        st.plotly_chart(draw_scatter(col_scatter3, col_scatter4, region2))
        
    col11, col12, col13, col14, col15, col16, col17 = st.columns([3,3,3,1,3,3,3])
    
    with col11:
        region3 = st.selectbox('Sélectionnez une région', ('Europe', 'USA', 'Japon', 'Global'), key=31, index=1)
    
    with col12:
        col_scatter5 = st.selectbox('Sélectionnez l\'axe x', cols, key=32, index=3)
        
    with col13:
        col_scatter6 = st.selectbox('Sélectionnez l\'axe y', cols, key=35, index=4)
        
    with col15:
        region4 = st.selectbox('Sélectionnez une région', ('Europe', 'USA', 'Japon', 'Global'), key=33, index=2)
    
    with col16:
        col_scatter7 = st.selectbox('Sélectionnez l\'axe x', cols, key=34, index=4)
        
    with col17:
        col_scatter8 = st.selectbox('Sélectionnez l\'axe y', cols, key=36, index=2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(draw_scatter(col_scatter5, col_scatter6, region3))
        
    with col2:
        st.plotly_chart(draw_scatter(col_scatter7, col_scatter8, region4))
        
    "On retrouve ici le même type d'information que sur la page précédente, mais de façon plus facilement comparable. Il est intéressante de noter ceci dit l'évolution au fil des années, en particulier pour les voitures américaines, avec une tendance à la normalisation de la puissance et de la consommation, très probablement en conséquence aux deux chocs pétroliers de 1973 et 1979."

if __name__ == "__main__":
    main()