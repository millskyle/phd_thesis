


cd /home/kmills/git/phd_thesis/
#local_loc='/Users/kmills/Documents/bibtex/KMPhD.bib'

local_loc='/home/kmills/bibtex/KMPhD.bib'

if ! $(diff $local_loc ./); then
	cp $local_loc ./
	git add $(basename $local_loc) \
	&& git commit -m "automatic bib commit" \
	&& git push
fi
date > last_committed.log
