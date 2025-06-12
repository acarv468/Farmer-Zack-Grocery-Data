# Farmer Zack Grocery Store Case Study

The **Farmer Zack Grocery Store Case Study** project is a data pipeline and analytics case study designed to generate, process, and upload dummy grocery store data to Google BigQuery and visualize the data in Looker Studio. 

**[Farmer Zack Sales Dashboard](https://lookerstudio.google.com/reporting/96b1dd92-f479-417a-97c9-e45915107d0f)**

## Background and Design

**Farmer Zack** is a reference to Detroiters Season 2 Episode 5. https://www.imdb.com/title/tt7692336/. 

The **Farmer Zack Sales Dashboard** was designed with clarity, accessibility, and actionable insights in mind. The layout prioritizes key performance indicators (KPIs) at the top, providing an at-a-glance summary of revenue, visitors, basket size, and conversion rates. Below, a series of time-based and categorical charts allow users to quickly identify trends and outliers across locations, product categories, and individual products.

### Accessibility and Color Choices

Instead of the traditional green and red to indicate positive and negative changes, the dashboard uses **blue** for increases and **orange** for decreases. I chose this color scheme because blue and orange are more easily distinguishable for most types of color blindness, ensuring that all users can interpret the data accurately. The use of clear icons and consistent formatting further enhances readability and user experience.

![farmer_zack](farmer-zack.jpeg "Farmer Zack")

## Features

- **Data Generation**: Creates realistic dummy data for stores, products, foot traffic, and transactions.
- **BigQuery Integration**: Uploads the generated data to Google BigQuery tables for further analysis.
- **Environment Configuration**: Uses a `.env` file to manage sensitive credentials and project settings.
- **Data Cleaning**: Clears existing data in BigQuery tables before uploading new data.
- **Customizable**: Easily modify the data generation logic to suit specific use cases.

## Requirements

- Python 3.8 or higher
- Google BigQuery Python Client Library
- Pandas
- dotenv

## BigQuery Tables and Views

### Tables
- `stores`: Contains store IDs and locations.
- `products`: Contains product details such as name and category.
- `foot_traffic`: Contains daily visitor counts for each store.
- `transactions`: Contains transaction details, including product, quantity, and price.

### Views
- `transaction_details`: an aggregated view of transactions joined with store and product details
- `transaction_summaries`: a daily aggregated summary of transactions by store with visitor counts included
