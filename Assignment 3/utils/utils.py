def write_news_to_markdown(news_articles, filename):
    """This function takes news articles list and write it in MD file format"""
    with open(filename, 'w', encoding='utf-8') as file:
        for category in news_articles:
            # Write the category as a main header(# defines header in md **text** for bold)
            file.write(f"# **{category['category']}**\n\n")
            #counter is used to number the articles in the category
            count = 1
            
            #This loop iterates for each article of catergory and writes it in file
            for article in category['articles']:
                #Write title of the article
                file.write(f'#### **{count}. [{article['title']}]({article['link']})**\n\n')
                count+=1
                
                # Write the body of the article
                file.write(f"{article['body']}\n\n")