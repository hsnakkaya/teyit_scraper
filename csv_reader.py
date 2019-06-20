import csv
import pprint

with open('articles.csv', 'r', encoding="utf8") as f:
    readCSV = csv.reader(f, delimiter=',')

    header = True

    tag_nodes = []
    author_nodes = []
    article_nodes = []
    claim_nodes = []
    idda = 0
    artic = 0

    author_node_header = ['Type', 'Name']
    tag_node_header = ['Type', 'Name', 'URL']
    article_node_header = ['Type', 'Name', 'URL', 'Date']
    claim_node_header = ['Type', 'Name', 'URL', 'Date', 'Claim', 'Verdict']
    edges_node_header = ['FromType', 'FromName', 'Edge', 'ToType', 'ToName']

    with open('nodes/edges.csv', mode='w', encoding='utf-8', newline='') as edges_file:
        edges_writer = csv.DictWriter(edges_file, fieldnames=edges_node_header)
        edges_writer.writeheader()
        edges_writer = csv.writer(edges_file)

        with open('nodes/claim_nodes.csv', mode='w', encoding='utf-8', newline='') as claim_file:
            claim_writer = csv.DictWriter(claim_file, fieldnames=claim_node_header)
            claim_writer.writeheader()
            claim_writer = csv.writer(claim_file)

            with open('nodes/article_nodes.csv', mode='w', encoding='utf-8', newline='') as article_file:
                article_writer = csv.DictWriter(article_file, fieldnames=article_node_header)
                article_writer.writeheader()
                article_writer = csv.writer(article_file)

                with open('nodes/author_nodes.csv', mode='w', encoding='utf-8', newline='') as file:
                    csv_writer = csv.DictWriter(file, fieldnames=author_node_header)
                    csv_writer.writeheader()
                    csv_writer = csv.writer(file)

                    with open('nodes/tag_nodes.csv', mode='w', encoding='utf-8', newline='') as tag_file:
                        csv_tag_writer = csv.DictWriter(tag_file, fieldnames=tag_node_header)
                        csv_tag_writer.writeheader()
                        csv_tag_writer = csv.writer(tag_file)

                        for row in readCSV:
                            if header:
                                header = False
                            else:
                                author = row[0]
                                claim = row[1]
                                date = row[2]
                                img_link_list = row[3]
                                is_claim = row[4]
                                link_list = row[5]
                                tags = row[6]
                                text_all = row[7]
                                title = row[8]
                                url = row[9]
                                verdict = row[10]

                                if is_claim == 'True':
                                    print('this is a claim ')
                                    category = 'Claim'

                                    claim_node = [category, title, url, date, claim, verdict]
                                    claim_nodes.append(claim_node)
                                    claim_writer.writerow(claim_node)

                                elif is_claim == 'False':
                                    print('this is an article ')
                                    category = 'Article'

                                    article_node = [category, title, url, date]
                                    article_nodes.append(article_node)
                                    article_writer.writerow(article_node)

                                edge = [category, title, 'Was Written By', 'Author', author]
                                edges_writer.writerow(edge)

                                tag = tags.replace('[', '').replace(']', '').replace("'", '')
                                tag = tag.split(',')

                                for i in range(len(tag)):
                                    if i % 2 == 0:
                                        print('tag: ', tag[i])
                                        tag_text = tag[i]
                                    else:
                                        print('url: ', tag[i])
                                        tag_url = tag[i]
                                        tag_node = ['Tag', tag_text, tag_url]
                                        csv_tag_writer.writerow(tag_node)

                                        edge = [category, title, 'Is tagged', 'Tag', tag_text]
                                        edges_writer.writerow(edge)

                                author_node = ['Author', author]
                                author_nodes.append(author_node)

                        skt = set(tuple(i) for i in author_nodes)
                        pprint.pprint(skt)

                        for authors in skt:
                            csv_writer.writerow(authors)
