build:
	docker build -t awsbatch/myblast:latest .
	docker tag awsbatch/myblast:latest 652462447887.dkr.ecr.us-east-1.amazonaws.com/awsbatch/myblast:latest
	docker push 652462447887.dkr.ecr.us-east-1.amazonaws.com/awsbatch/myblast:latest

run:
	aws batch submit-job --job-name j2 --job-queue robq --job-definition myblast:2

