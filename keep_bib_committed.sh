


local_loc='/home/kmills/bibtex/KMPhD.bib'

cp $local_loc ./
git add $(basename $local_loc)
git commit -m "automatic bib commit"
git push

