if  [[ "$1" = "bash" || "$1" = "sh"  ]]
then
	exec /bin/sh --login -i
fi