def get_id():
    with open("movie_url.txt", encoding="utf-8") as f_in, open("movie_id.csv", "w+", encoding="utf-8") as f_out:
        url_list = f_in.readlines()
        for url in url_list:
            name = url.strip().split("\t")[0]
            id = url.strip().split("cover/")[1].split(".")[0]
            f_out.write("".join([name, "\t", id, "\n"]))


if __name__ == '__main__':
    get_id()
