import requests
from lib import login, logout, search, link_crawler
from custom_ui import print_ui, user_warning, items_list
from time import sleep
from bs4 import BeautifulSoup

def generate_links(session, search_type, search_term):
    items = search(session, search_type, search_term)
    items_list(items, search_type)
    selection = int(input('Enter the item count to generate links:'))
    print('\n\n')
    if search_type == 'series':
        crawled_links = link_crawler(session=session, select_url=items[selection][1]['item_url'] + '/')
        item_name = items[selection][1]['item_name']
        with open(f'GeneratedLinks/{item_name}_links.txt', 'a+') as file:
            for link in crawled_links:
                file.write(link + '\n')
            file.close()
        print(f'Links generated for {item_name}')
    elif search_type == 'movies':
        movie_player = session.get(url=primary_url + items[selection][1]['item_url'], headers=dflix_headers)
        movie_player_soup = BeautifulSoup(movie_player.text, "html.parser")
        item_name = items[selection][1]['item_name']
        with open(f'GeneratedLinks/{item_name}_links.txt', 'a+') as file:
            file.write(movie_player_soup.find('source')['src'] + '\n')
            file.close()
        print(f'Links generated for {item_name}')
    print('Saved to GeneratedLinks folder.')
    sleep(1)
    clear()

def main():
    with requests.Session() as session:
        print_ui()
        user_warning()
        session = login(session)
        sleep(1)
        clear()
    while True:
        get_profile_info(session)
        print_ui()
        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
        except ValueError:
            print("INVALID CHOICE!")
            sleep(1)
            clear()
            print("Returning to the main menu!")
            sleep(1)
            continue
        if choice == 1:  # re-login
            relogin(session)
        elif choice == 2:  # generate links: series
            generate_links(session, 'series', input("Enter any word to search: "))
        elif choice == 3:  # generate links: movies
            generate_links(session, 'movies', input("Enter any word to search: "))
        elif choice == 4:
            logout(session)
            continue
        elif choice == 5:
            clear()
            print("Exiting...")
            sleep(1)
            print('The program exited successfully!')
            break
    return 0

if __name__ == '__main__':
    main()
