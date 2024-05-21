import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import time

airbnb_df = pd.read_csv('Airbnb.csv')

# Add a title to your Streamlit app
st.markdown('<h1 style="color:#B22222;">AIRBNB</h1>', unsafe_allow_html=True)

# Display a Font Awesome icon
font_awesome_css = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"
st.markdown(f'<link href="{font_awesome_css}" rel="stylesheet">', unsafe_allow_html=True)
st.markdown('<i class="fas fa-check-circle" style="font-size:50px;color:orange;"></i>', unsafe_allow_html=True)

# Rest of your Streamlit app code
st.write("Best prices on Hotels")
st.write("Book & Enjoy your Stays with AIRBNB! \U0001F600")

#set up home page and optionmenu 
selected = option_menu("",
                        options=["Home","Explore Hotels","EDA","Top Insights","About Us"],
                        icons=["house","search","check","lightbulb","info-circle"],
                        default_index=1,
                        orientation="horizontal",
                            styles={
                                    "container": {"width": "100%", "border": "2px ridge", "background-color": "#B22222"},
                                    "icon": {"color": "#F8CD47", "font-size": "20px"}, 
                                    "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "color": "#FFFFFF"},  # Regular text color
                                    "nav-link-selected": {"background-color": "#000000", "color": "#FFFFFF"},  # Selected option text and background color
                                })

if selected == "Home":

    st.subheader("Airbnb revolves around providing unique and personalized travel experiences through a platform that connects hosts with travelers worldwide!")
    
    st.subheader(":red[**Why AIRBNB ? :**]")
    st.write("1. :blue[**Local Immersion :**] Airbnb emphasizes the opportunity for travelers to immerse themselves in local culture by staying in accommodations hosted by locals. This goes beyond just lodging, offering insights into neighborhoods, customs, and lifestyles.")
    st.write("2. :blue[**Diversity and Choice :**] Airbnb's platform offers a diverse range of accommodations, from apartments and houses to unconventional options like castles or houseboats. This variety allows travelers to find accommodations that suit their preferences and budget.")
    st.write("3. :blue[**Community and Connection :**] Airbnb fosters a sense of community between hosts and guests, encouraging meaningful interactions and cultural exchange. This can lead to memorable experiences and lasting connections.")
    st.write("4. :blue[**Flexibility and Personalization :**] The platform provides flexibility in terms of check-in/check-out times, house rules, and amenities, allowing guests to tailor their stay to their needs. Hosts often offer personalized recommendations and hospitality.")
    st.write("5. :blue[**Trust and Safety :**] Airbnb prioritizes trust and safety through features like verified profiles, secure payment systems, and reviews from previous guests. This helps build confidence and transparency in the booking process.")
    st.write("6. :blue[**Global Reach :**]  With listings in over 220 countries and regions, Airbnb offers a global reach that allows travelers to explore diverse destinations and accommodations worldwide.")
    
    st.subheader(':red[Information :]')
    st.markdown('''**This Project - Airbnb Analysis was done by myself, Arivalagan L**''')
    st.markdown('''**To refer codes of this project, refer my Github page by clicking on the button below**''')
    st.link_button('Go to Github','https://github.com/Arivalagan16') 

if selected == "Explore Hotels":
        
    Maps = ['--Select--','Global View of Total Hotel Count in Every Countries','Explore Hotels']

    # Create a dropdown select box
    selected_option = st.selectbox('Select an option:', Maps)

    if selected_option == "Global View of Total Hotel Count in Every Countries":
        
        data = airbnb_df[['Name','Country','Latitude','Longitude']]
        df=pd.DataFrame(data)

        hotel_count_df = airbnb_df.groupby('Country')['Name'].count().reset_index()

        hotel_count_df.columns = ['Country', 'Hotel Count']

        df['TotalHotels'] = df.groupby('Country')['Name'].transform('count')

        # Plotting geographical plot
        fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', hover_name='Country',
                                color='TotalHotels', size='TotalHotels',
                                title='Global View of Total Hotel Count in Every Countries',
                                projection='orthographic',
                                color_continuous_scale='Rainbow')
        
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(hotel_count_df[['Country', 'Hotel Count']].reset_index(drop=True))


    if selected_option == 'Explore Hotels':

        clm=airbnb_df[['Country']]

        Country_df = pd.DataFrame(clm)
        
        selected_country= st.selectbox("Choose Destination",options=Country_df['Country'].unique())

        filtered_df = airbnb_df[airbnb_df['Country'] == selected_country]

        property_types = filtered_df['Property_type'].unique()
        selected_property_types = st.multiselect('Choose Property Type', property_types)

        # Filter DataFrame based on selected property types
        if selected_property_types:
            filtered_df = filtered_df[filtered_df['Property_type'].isin(selected_property_types)]

        filtered_df = filtered_df.sort_values(by='Price', ascending=False)

        if not filtered_df.empty:
            # Center the map on the selected country
            avg_lat = filtered_df['Latitude'].mean()
            avg_lon = filtered_df['Longitude'].mean()

            fig = px.scatter_geo(
                filtered_df,
                lat='Latitude',
                lon='Longitude',
                text='Name',
                size='Price',
                color='Property_type',
                hover_name='Property_type',
                hover_data={'Price': True, 'Property_type': True},
                title=f"Hotels in {selected_country} by Property_type",
                size_max=15,
                color_continuous_scale='Rainbow')
            fig.update_layout(
                mapbox=dict(
                    center=dict(lat=avg_lat, lon=avg_lon),
                    zoom=5  # Adjust zoom level as needed
                ),
            )
            st.plotly_chart(fig)

            st.write('**Name of Hotels and its Price**')

            st.dataframe(filtered_df[['Name', 'Price']].reset_index(drop=True))

        else:
                st.write('No data available for the selected filters.')


if selected == "EDA":

    opt=["Statistical Summary of Price",
            "Mean Price of Hotel Rooms in Every Countries",
            "Average Price of all Room Types",
            "Average Rating of all Property Types",
            "Correlation Matrix",
            "Covariance Matrix"
        ]
    
    query=st.selectbox(':blue[Select]',options=opt,index=None)

    if query == opt[0]:

        Price=airbnb_df['Price']

        avg_price = np.average(Price)
        var_price = np.var(Price)
        std_price = np.std(Price)
        median_price = np.median(Price)
        min_price = np.min(Price)
        max_price = np.max(Price)

        # Create a dictionary with the statistical values
        stats_dict = {
            'Statistics': ['Average Price', 'Standard Deviation', 'Median Price', 'Minimum Price', 'Maximum'],
            'Values': [avg_price, std_price, median_price, min_price, max_price]
        }

        # Create a DataFrame from the dictionary
        stats_df = pd.DataFrame(stats_dict)

        # Prepare data for plotting
        statistics = {
            'Average Price': avg_price,
            'Standard Deviation': std_price,
            'Median Price': median_price,
            'Min Price': min_price,
            'Max Price': max_price}


        # Create Plotly horizontal bar chart
        fig = go.Figure(go.Bar(
            x=list(statistics.values()),
            y=list(statistics.keys()),
            orientation='h',
            marker=dict(color=['skyblue', 'orange', 'green', 'red', 'purple', 'brown']),
            hoverinfo='x+y',
            text=list(statistics.values()),
            textposition='auto'))

        # Update layout
        fig.update_layout(
            title='Summary Statistics for Price',
            xaxis_title='Values',
            yaxis_title='Statistics',
            yaxis=dict(tickmode='linear'))

        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(stats_df,hide_index=True)

    if query == opt[1]:

        grouped_data = airbnb_df.groupby('Country')['Price'].mean().reset_index()
        Coun_price_df=pd.DataFrame(grouped_data)

        Coun_price_df.rename(columns={'Price': 'Mean_Price'}, inplace=True)

        # Create Plotly plot with hover functionality
        fig = px.bar(Coun_price_df, x='Country', y='Mean_Price', color='Mean_Price', 
                        title='Average Price of Hotels in Various Countries',
                        labels={'Country': 'Country', 'Mean_Price': 'Mean Price'},
                        color_continuous_scale='pinkyl')

        # Update layout to match the desired aesthetics
        fig.update_layout(
            xaxis_title='Country',
            yaxis_title='Mean Price',
            xaxis=dict(tickangle=45)
        )

        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(Coun_price_df,hide_index=True)

    if query == opt[2]:

        grouped_data = airbnb_df.groupby('Room_type')['Price'].mean().reset_index()
        rt_price_df=pd.DataFrame(grouped_data)

        # Create Plotly bar plot with hover functionality
        fig = px.bar(rt_price_df, x='Room_type', y='Price', 
                        title='Average Price of all Room Types',
                        labels={'Room_type': 'Room Type', 'Price': 'Price'},
                        color='Price',  
                        color_continuous_scale='viridis') 

        # Update layout to match the desired aesthetics
        fig.update_layout(
            xaxis_title='Room Type',
            yaxis_title='Price',
            xaxis=dict(tickangle=45))

        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(rt_price_df,hide_index=True)

    if query == opt[3]:

        grouped_data = airbnb_df.groupby('Property_type')['Rating'].mean().reset_index()
        pt_rating_df = pd.DataFrame(grouped_data)

        # Plotly Express bar chart with hovering
        fig = px.bar(grouped_data, x='Property_type', y='Rating', color='Property_type',
                        title='Average Ratings of all Property Types',
                        labels={'Property_type': 'Property Type', 'Rating': 'Rating'},
                        hover_name='Property_type', hover_data={'Rating': True})

        # Customize layout if needed
        fig.update_layout(xaxis_title='Property Type', yaxis_title='Rating', xaxis_tickangle=60)

        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(pt_rating_df,hide_index=True)

    if query == opt[4]:

        col1,col2 = st.columns(2)

        with col1:

            Selected_columns= airbnb_df[['Price','Accomodates','Bedrooms','Beds','Bathrooms','Cleaning_fee']]

            room_df=pd.DataFrame(Selected_columns)

            # Let's start by calculating the correlation matrix

            correlation_matrix = room_df.corr()

            fig, ax = plt.subplots(figsize=(4,2))

            heatmap = sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, annot_kws={"size": 5})
            ax.set_title('Correlation between Room Price and Key Room structures', fontsize=6)
            ax.tick_params(axis='both', which='major', labelsize=5)
            cbar = heatmap.collections[0].colorbar
            cbar.ax.tick_params(labelsize=5)
            st.pyplot(fig)

        with col2:

            columns=airbnb_df[['Price','Total_reviews','Overall_score','Cleanliness_score','Location_score','Rating']]

            review_df=pd.DataFrame(columns)

            correlation_matrix = review_df.corr()
            fig, ax = plt.subplots(figsize=(4,2))

            heatmap = sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
                                    annot_kws={"size": 5} )
            ax.set_title('Correlation Matrix between Price and Ratings',  fontsize=6)
            ax.tick_params(axis='both', which='major', labelsize=5)
            cbar = heatmap.collections[0].colorbar
            cbar.ax.tick_params(labelsize=5)
            st.pyplot(fig)

    if query == opt[5]:

        col1,col2 = st.columns(2)

        with col1:

            Selected_columns= airbnb_df[['Price','Accomodates','Bedrooms','Beds','Bathrooms','Cleaning_fee']]

            room_df=pd.DataFrame(Selected_columns)

            # Let's start by calculating the correlation matrix

            corvariance_matrix = room_df.cov()

            fig, ax = plt.subplots(figsize=(4,2))

            heatmap = sns.heatmap(corvariance_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, annot_kws={"size": 5})
            ax.set_title('Covariance between Room Price and Key Room structures', fontsize=6)
            ax.tick_params(axis='both', which='major', labelsize=5)
            cbar = heatmap.collections[0].colorbar
            cbar.ax.tick_params(labelsize=5)
            st.pyplot(fig)

        with col2:

            columns=airbnb_df[['Price','Total_reviews','Overall_score','Cleanliness_score','Location_score','Rating']]

            review_df=pd.DataFrame(columns)

            covariance_matrix = review_df.cov()

            fig, ax = plt.subplots(figsize=(4,2))

            heatmap = sns.heatmap(covariance_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
                                    annot_kws={"size": 5} )
            ax.set_title('Covariance Matrix between Price and Ratings',  fontsize=6)
            ax.tick_params(axis='both', which='major', labelsize=5)
            cbar = heatmap.collections[0].colorbar
            cbar.ax.tick_params(labelsize=5)
            st.pyplot(fig)

if selected == "Top Insights":

    opt=["Top 10 Expensive Hotel rooms",
            "Top 10 Affordable Hotel Rooms",
            "Total Count of Hotels Listed in Every Countries",
            "10 Leading Host Names with Highest Host Listings",
            "Hotel Counts with Top most Ratings",
            "Toprated 10 Hotel Names with Country Codes",
            "Average Avilability of Hotel Rooms in Every Countries per month",
            "Room types with Maximum Ratings in Every Countries"]
    
    query=st.selectbox(':blue[Select]',options=opt,index=None)

    def stream1():
            for i in t_1:
                yield i + ''
                time.sleep(0.02)
    def stream2():
            for i in t_2:
                    yield i + ''
                    time.sleep(0.02)
    def stream3():
            for i in t_3:
                    yield i + ''
                    time.sleep(0.02)

    if query == opt[0]:

        col1,col2=st.columns(2)

        with col1:

            clm=airbnb_df[['Name','Price','Country']]
            df=pd.DataFrame(clm)

            sorted_df=df.sort_values(by="Price", ascending=False)

            top_10_rows=sorted_df.head(10)

            new_df = top_10_rows.reset_index(drop=True)

            top_10_hotels=pd.DataFrame(new_df)

            # Plotly bar chart with hovering
            fig = px.bar(top_10_hotels, x='Name', y='Price', hover_data={'Price': ':.2f'},
                            labels={'Name': 'Hotel Name', 'Price': 'Price'},
                            title='Top 10 Expensive Hotel rooms',
                            color='Country',color_continuous_scale='rainbow')
            fig.update_layout(xaxis_title='Hotel Name', yaxis_title='Price')

            st.plotly_chart(fig,use_container_width=True)
            st.dataframe(top_10_hotels,hide_index=True)
        
        with col2:
            
            fig=px.pie(top_10_hotels,names='Name',values='Price',color='Country',
            title='Percentage of Top 10 Expensive Hotel rooms',
            color_discrete_sequence=px.colors.cmocean.balance_r)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig,use_container_width=True)

            st.markdown('<br>', unsafe_allow_html=True)

            t_1='''1. Turkey: "Center of Istanbul Sisli" stands out as the most expensive accommodation with a price of 48,842 Turkish Lira,
            reflecting its prime location in the heart of Istanbul's vibrant Sisli district.'''                                   
            
            t_2='''2. Hong Kong: The city boasts several high-priced accommodations, including "HS1-2人大床房+丰泽､苏宁､百脑汇+女人街+美食中心" and 
            "良德街3号温馨住宅" priced at 11,681 Hong Kong Dollars each, suggesting a strong demand.'''               
            
            t_3='''3. Brazil: Not to be outdone, Brazil features luxurious accommodations like "Apartamento de luxo em Copacabana - 4 quartos" and "Deslumbrante apartamento na AV.Atlantica"
            with prices exceeding 6,000 Brazilian Reais.'''
            

            st.write_stream(stream1())
            st.write_stream(stream2())
            st.write_stream(stream3())

    if query == opt[1]:

        col1,col2=st.columns(2)
        with col1:

            clm=airbnb_df[['Name','Price','Country']]
            df=pd.DataFrame(clm)

            sorted_df=df.sort_values(by="Price")

            top_10_rows=sorted_df.head(10)


            new_df = top_10_rows.reset_index(drop=True)

            top_10_hotels_low=pd.DataFrame(new_df)

            # Plotly bar chart with hovering
            fig = px.bar(top_10_hotels_low, x='Name', y='Price', hover_data={'Price': ':.2f'},
                            labels={'Name': 'Hotel Name', 'Price': 'Price'},
                            title='Top 10 Affordable Hotel Rooms',
                            color='Country',color_continuous_scale='viridis')
            fig.update_layout(xaxis_title='Hotel Name', yaxis_title='Price')

            st.plotly_chart(fig,use_container_width=True)
            st.dataframe(top_10_hotels_low,hide_index=True)

        with col2:
            
                fig=px.pie(top_10_hotels_low,names='Name',values='Price',color='Country',
                        title='Percentage of Top 10 Affordable Hotel Rooms',
                        color_discrete_sequence=px.colors.cmocean.balance_r)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

                st.markdown('<br>', unsafe_allow_html=True)

                t_1='''1. Among the top 10 Affordable Hotel Rooms, the most budget-friendly options are found in Portugal and Spain.'''
                
                t_2='''2. Portugal offers the most affordable accommodations, with prices ranging from  9 to 13 dollers.'''
                
                t_3='''3. Spain also provides reasonable priced options, with room rates ranging from 10 to 12 dollers.'''
                
                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())

            

    if query == opt[2]:

            hotel_count = airbnb_df['Country'].value_counts().reset_index()
            hotel_count.columns = ['Country', 'Count']

            fig = px.pie(hotel_count, values='Count', names='Country',
                            labels={'Country': 'Country'},
                            title='Total Count of Hotels Listed in Every Countries')
            
            st.plotly_chart(fig,use_container_width=True)

            st.write(":blue[**Top 3 countries with Maximum number of Hotels :**]")

            t_1="1. United States Tops the list with 1222 Hotel Rooms"
            t_2="2. Turkey follows Us with 661 Rooms"
            t_3="3. Canada follows Turkey in the list with 649 Rooms"

            st.write_stream(stream1())
            st.write_stream(stream2())
            st.write_stream(stream3())

    if query == opt[3]:

        host_listings_count = airbnb_df['Host_name'].value_counts().reset_index()
        host_listings_count.columns = ['Host_name', 'Host_total_listings']

        # Identify the host name with the highest count
        highest_host_name = host_listings_count.loc[0, 'Host_name']
        highest_host_count = host_listings_count.loc[0, 'Host_total_listings']

        top_10_hosts = host_listings_count.head(10)

        # Plotting the host name with the highest count using Plotly with hovering
        fig = px.pie(top_10_hosts, values='Host_total_listings', names='Host_name',
                        labels={'Host_name': 'Host Name', 'Host_total_listings': 'Listing Count'},
                        title='10 Leading Host Names with Highest Host Listings')
        
        st.plotly_chart(fig,use_container_width=True)

        st.write(":blue[**Top 3 Host Names with Maximum Listing Counts:**]")

        t_1="1. Maria Tops the list with 37 Listing Counts"
        t_2="2. David follows Us with 36 Listing Counts"
        t_3="3. JOv follows Turkey in the list with 21 Listing Counts"

        st.write_stream(stream1())
        st.write_stream(stream2())
        st.write_stream(stream3())

    if query == opt[4]:
        
        col1,col2=st.columns(2)
        with col1:

                    rating_counts = airbnb_df['Rating'].value_counts().reset_index()
                    rating_counts.columns = ['Rating', 'Id']

                    sorted_df=rating_counts.sort_values(by="Rating", ascending=False)

                    top_10_ratings = sorted_df.head(10).reset_index(drop=True)

                    # Plotting hotel count by rating using Plotly bar chart
                    fig = px.bar(top_10_ratings, x='Rating', y='Id',
                                    labels={'Rating': 'Rating', 'Id': 'Hotel Count'},
                                    title='Hotel Counts with Top most Ratings',
                                    color='Rating',color_continuous_scale='thermal')

                    fig.update_layout(xaxis_title='Rating', yaxis_title='Hotel Count')
                    st.plotly_chart(fig,use_container_width=True)

        with col2:
                    fig = px.pie(top_10_ratings, values='Rating', names='Id',
                        labels={'Rating': 'Rating', 'Id': 'Hotel Count'},
                        title='Percentage of Hotel Counts with Top most Ratings',
                        color='Rating')

                    fig.update_layout(xaxis_title='Rating', yaxis_title='Hotel Count')
                    st.plotly_chart(fig,use_container_width=True)

                    t_1="1. In the 1st Position, There are 982 Hotels listed with 100 rating rate"
                    t_2="2. Following Next, There are 291 Hotels listed with 98 rating rate"
                    t_3="3. Setting up in the 3rd, There are 281 Hotels listed with 97 rating rate"

                    st.write_stream(stream1())
                    st.write_stream(stream2())
                    st.write_stream(stream3())

    if query == opt[5]:

        col1,col2=st.columns(2)
        with col1:           

            clm=airbnb_df[['Name','Rating',"Country_code"]]

            df=pd.DataFrame(clm)

            # Identify the top 10 hotels with maximum ratings
            top_10_hotels = df.sort_values(by='Rating', ascending=False).head(10)

            # Create the bar chart
            fig = px.bar(top_10_hotels, x='Name', y='Rating',
                        labels={'Name': 'Hotel Name', 'Rating': 'Rating'},
                        title='Toprated 10 Hotel Names with Country Codes',
                        color='Country_code',
                        color_continuous_scale='Viridis')

            fig.update_layout(xaxis_title='Hotel Name', yaxis_title='Rating')

            st.plotly_chart(fig,use_container_width=True)
            st.dataframe(top_10_hotels,hide_index=True)

        with col2:
                    fig = px.pie(top_10_hotels, values='Rating', names='Name',
                        labels={'Name': 'Hotel Name', 'Rating': 'Rating'},
                        title='Percentage of Toprated 10 Hotel Names with Country Codes',
                        color='Country_code')

                    fig.update_layout(xaxis_title='Name', yaxis_title='Rating')
                    st.plotly_chart(fig,use_container_width=True)

                    t_1="1. Very sunny 3 bedroom in Rosemont, From CA, California, Tops the list with Maximum Ratings."
                    t_2="2. Following Very sunny 3 bedroom in Rosemont , Bright Cosy Flat in Batalha | Ace Location, from PT, Portugal hinches the 2nd Position."
                    t_3="3. Setting up the line in the 3rd, Swimming Pool/ Amazing Layout W&D Doorman 5131, from US, United States, Holds the third Position."

                    st.write_stream(stream1())
                    st.write_stream(stream2())
                    st.write_stream(stream3())


    if query == opt[6]:

        col1,col2=st.columns(2)

        with col1:

            columns=airbnb_df[['Country','Availability_30']]

            df=pd.DataFrame(columns)

            avg_availability_by_country = df.groupby('Country')['Availability_30'].mean().reset_index()

            df1= avg_availability_by_country.sort_values(by='Availability_30', ascending=False).head(10)

            # Create the sunburst plot
            fig = px.sunburst(df1, path=['Country'], values='Availability_30',
                            color='Availability_30',  # Color by availability
                            color_continuous_scale='turbid',  # Optional: Apply a color scale
                            labels={'Availability_30': 'Average Availability'},
                            title=("Average Avilability of Hotel Rooms in Every Countries per month"))

            fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
            st.plotly_chart(fig,use_container_width=True)
            st.dataframe(df1,hide_index=True)

        with col2:
            
                t_1="1. Hotels in Turkey. Tops the Position with maximum availability of 22 days per month"
                t_2="2. Hotels in China, Second tops the List with maximum availability of 19 days in a month."
                t_3="3. Following China ,Portugal holds the 3rd Position with availability of 16 days."

                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
        

    if query == opt[7]:

        col1,col2=st.columns(2)
        with col1:

            clm=airbnb_df[['Room_type','Rating','Country']]

            df=pd.DataFrame(clm)

            # Get the top-rated room type for each country
            top_rooms = df.groupby('Country').apply(lambda x: x.loc[x['Rating'].idxmax()]).reset_index(drop=True)


            # Plotting
            fig = px.bar(top_rooms, x='Country', y='Rating', color='Room_type',
                            title='Room types with Maximum Ratings in Every Countries',
                            labels={'Rating': 'Maximum Rating', 'Room_type': 'Room Type'})
            st.plotly_chart(fig,use_container_width=True)
            st.dataframe(top_rooms,hide_index=True)

        with col2:
            
            fig = px.sunburst(top_rooms, path=['Country'], values='Rating',
                    color='Room_type', 
                    color_continuous_scale='turbid',
                    labels={'Rating': 'Maximum Rating', 'Room_type': 'Room Type'},
                    title='Room types with Maximum Ratings in Every Countries')

            fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
            st.plotly_chart(fig,use_container_width=True)

            t_1="1. In Australia, The Top rated Room Type is Entire Home / Apartment"
            t_2="2. In Brazil, The Top rated Room Type is Private Room."
            t_3="3. In Canada, The Top rated Room Type is Private Room."

            st.write_stream(stream1())
            st.write_stream(stream2())
            st.write_stream(stream3())

if selected == 'About Us':

        st.subheader(':red[History of AIRBNB]')
        st.markdown('''Airbnb has an interesting history that traces back to its founding in 2008. Here's a brief overview:
                    
Founding: Airbnb was founded by Brian Chesky, Joe Gebbia, and Nathan Blecharczyk. The idea came about when they couldn't afford their San Francisco apartment rent, so they decided to rent out air mattresses in their living room to attendees of a design conference. This led to the concept of "Air Bed and Breakfast," which later evolved into Airbnb.

Early Days: In 2009, Airbnb received its first funding and started to expand beyond air mattresses to include entire homes and apartments. They also introduced features like user profiles, host reviews, and secure payment systems.

Growth and Funding: Airbnb experienced rapid growth, expanding globally and attracting significant investments. By 2011, they were valued at over $1 billion.

Challenges and Regulation: As Airbnb grew, it faced challenges with regulatory issues in various cities and countries. Some areas imposed restrictions or bans on short-term rentals, citing concerns about housing availability, safety, and tax compliance.

Diversification: Over time, Airbnb diversified its offerings to include experiences, where hosts can offer unique activities to guests, such as guided tours, cooking classes, and workshops.

Impact and Innovation: Airbnb has had a significant impact on the hospitality industry, disrupting traditional hotel models and providing alternative accommodation options for travelers. The company has also focused on sustainability initiatives and community engagement.

COVID-19 Pandemic: Like many travel-related businesses, Airbnb faced challenges during the COVID-19 pandemic, with a significant decline in bookings initially. However, they adapted by promoting longer-term stays, remote work options, and enhanced cleaning protocols.

IPO and Beyond: In December 2020, Airbnb went public with a highly anticipated initial public offering (IPO). Since then, the company has continued to innovate, expand its offerings, and navigate the evolving travel landscape.

Overall, Airbnb's journey reflects the evolution of the sharing economy, the challenges of disruption, and the resilience required to succeed in a dynamic industry..''')


        st.subheader(':red[Policies of AIRBNB]')
        st.markdown('''
                    Guest Policies:

Booking and Payments: Guests must provide accurate information when booking, including the number of guests and payment details. Payments are typically made through Airbnb's secure platform.
House Rules: Guests are expected to follow the house rules set by hosts, which may include restrictions on smoking, pets, parties, and noise levels.
Reviews and Ratings: After a stay, guests can leave reviews and ratings for the host, and hosts can do the same for guests. This feedback system helps maintain accountability and transparency.

                    Host Policies:

Listing Guidelines: Hosts must provide accurate and detailed information about their property, including photos, amenities, house rules, and pricing.
Responsiveness: Hosts are expected to respond promptly to booking inquiries, messages from guests, and any issues that may arise during a guest's stay.
Hospitality Standards: Airbnb encourages hosts to provide a clean, comfortable, and welcoming environment for guests, along with clear communication and assistance when needed.

                    Safety and Security:

Identity Verification: Both guests and hosts may be required to verify their identity using Airbnb's verification process, which can include providing government-issued ID and other information.
Safety Features: Airbnb offers safety features such as secure payment processing, insurance coverage for hosts (in certain regions), and a 24/7 support team for assistance with safety-related concerns.
Community Standards: Airbnb has community standards that prohibit discriminatory behavior, harassment, illegal activities, and other violations. Users who violate these standards may face account suspension or removal from the platform.

                    Cancellation and Refund Policies:

Cancellation Policies: Hosts can choose from different cancellation policies (e.g., flexible, moderate, strict) that determine the refund amount for cancellations by guests.
Refunds and Resolution: Airbnb may facilitate refunds or resolutions in cases of cancellations, disputes, or unforeseen circumstances that impact a guest's stay.

                    Legal and Regulatory Compliance:

Local Laws: Airbnb expects hosts and guests to comply with local laws, regulations, and tax requirements related to short-term rentals, accommodations, and hospitality services.
Terms of Service: Users must agree to Airbnb's Terms of Service, which outline their rights, responsibilities, and the terms governing the use of the platform.
These policies help create a trustworthy and accountable community within Airbnb, promoting positive experiences for everyone involved.''')
        

        st.subheader(':red[Visit Official AIRBNB]')
        st.link_button('AIRBNB WEBSITE','https://www.airbnb.co.in/')