for attr in LENGTH_KM ria_ha_csu riv_tc_csu sgr_dk_rav  
do
	export attr="$attr"
	echo $attr
	python3 translate.py
done
