import requests
import csv
import datetime
import argparse
import re


def add_datetime(file_name, time_format):
    """Accepts a desired file_name,
    then formats the filename to include the current date and time.
        Args:
            file_name : the file to be formatted.
            time_format : the format of date time to be used.
    """
    curr_date = datetime.datetime.now()
    str_date = curr_date.strftime(time_format)
    return str_date + "_" + file_name


def number_of_pages(links):
    splitted_link = links.split(",")
    needed_link = re.search('&page=(.*)>', splitted_link[1])
    return needed_link.group(1)


def list_to_csv(search_term,token):
    desired_filename = add_datetime("output1" + ".csv", '%Y%m%d_%H-%M-%S')
    with open(desired_filename, 'w+', newline='', encoding="utf-8") as csv_file:
        fieldnames_csv = ['Name', 'Description', 'URL', 'Language', 'Updated']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames_csv)
        writer.writeheader()
        lines = get_json_response(search_term,token)

        for line in lines:
            writer.writerow(line)


def get_json_response(search_term,token):
    json_list = []
    search_params = {'q': search_term, 'per_page': 100}
    header_params = {"authorization": "token " + token}
    response = requests.get(
        'https://api.github.com/search/repositories',
        params=search_params,
        headers=header_params
    )

    no_of_pages = number_of_pages(response.headers["Link"])
    for page in range(1, int(no_of_pages)):
        search_params = {'q': search_term, 'per_page': 100, 'page': page}
        response = requests.get(
            'https://api.github.com/search/repositories',
            params=search_params,
            headers=header_params
        )
        json_output = response.json()
        list_response = json_output['items']

        for item in list_response:
            json_dict = {'Name': item['name'], 'Description': item['description'], 'URL': item['url'],
                     'Language': item['language'], 'Updated': item['updated_at']}
            json_list.append(json_dict)
    return json_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search_pattern")
    parser.add_argument("token")
    args = parser.parse_args()

    list_to_csv(args.search_pattern,args.token)


if __name__ == '__main__':
    main()
