import time
import yaml

# should be called from the root dir
my_name = "Bangqi Fu"


def gen_pubs(pubs, type="", header=""):
    html = ""
    bold_my_name = "<b>" + my_name + "</b>"

    if type != "" and header != "":
        html += "<h3>%s</h3>\n" % type
    
    num_count = len(pubs)
    # show in reversed order
    for pub in (pubs):
        label = "[%s%d]" % (header, num_count)
        html += "<li data-label=\"%s\">\n" % label
        num_count -= 1

        assert "authors" in pub
        assert my_name in pub["authors"]
        html += pub["authors"].replace(my_name, bold_my_name) + ", "

        assert "title" in pub
        html += '"<i>' + pub["title"] + '</i>", '

        assert "conf" in pub or "jour" in pub
        conf_jour = pub["conf"] if "conf" in pub else pub["jour"]
        html += conf_jour + " "

        assert "abbr" in pub
        html += "(<b>" + pub["abbr"] + "</b> '"

        assert "year" in pub
        html += str(pub["year"]) + ") "

        if "award" in pub:
            html += "(<span style=\"color: rgb(205, 35, 35);\"><b>Best Paper Award Nomination</b></span>)"
        
        if "links" in pub:
            for text, link in pub["links"]:
                html += '[<a href="%s" target="_blank">%s</a>] ' % (link, text)
        
        html += "\n</li>\n"
    return html

def gen_awards(awards):
    html = ""

    # show in reversed order
    for award in (awards):
        html += "<li>\n"
            
        assert "award" in award
        html += award["award"]

        if "link" in award:
            assert "name" in award
            html += '<a href="%s" target="_blank">%s</a>' % (award["link"], award["name"])

        html += ", "
        
        assert "year" in award
        html += str(award["year"]) + ". "

        # if "other_info" in award:
        #     html += award["other_info"] + " "
        
        html += "\n</li>\n"
    return html


# load HTML template
with open("header.html", "r") as f:
    html_template = f.read()

# load pubs and awards
with open("res/pubs_conf.yaml", "r") as f:
    pubs_conf = yaml.safe_load(f)
with open("res/pubs_jour.yaml", "r") as f:
    pubs_jour = yaml.safe_load(f)
with open("res/awards.yaml", "r") as f:
    awards = yaml.safe_load(f)

pubs_conf_html = gen_pubs(pubs_conf, "Conference", "C")
pubs_jour_html = gen_pubs(pubs_jour, "Journal", "J")
awards_html = gen_awards(awards)

index_html = html_template.replace("__PUBS__", pubs_jour_html + pubs_conf_html).replace("__AWARDS__", awards_html)

# update time
index_html = index_html.replace("__UPDATE_TIME__", time.strftime("%b %d, %Y", time.localtime()))

with open("index.html", "w") as f:
    f.write(index_html)
f.close()