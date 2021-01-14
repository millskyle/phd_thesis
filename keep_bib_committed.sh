


local_loc='/Users/kmills/Documents/bibtex/KMPhD.bib'

cp $local_loc ./
git add $(basename $local_loc)
git commit -m "automatic bib commit"
git push

date > last_committed.log

