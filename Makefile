kappa-client:
	wget localhost:8010/openapi.json -O openapi-kappa.json
	rm -rf libs/kappa-client
	docker run --rm \
		-v "$(PWD):/local" openapitools/openapi-generator-cli generate \
		-i /local/openapi-kappa.json \
		-g python \
		-o /local/libs/kappa-client \
		--additional-properties=packageName=kappa_client \
		--additional-properties=projectName=kappa-client \
		--additional-properties=packageVersion=0.0.0
	rm -f libs/**/*requirements.txt
	rm -f libs/**/setup.*

kappa-data-client:
	wget localhost:8020/openapi.json -O openapi-kappa-data.json
	rm -rf libs/kappa-data-client
	docker run --rm \
		-v "$(PWD):/local" openapitools/openapi-generator-cli generate \
		-i /local/openapi-kappa-data.json \
		-g python \
		-o /local/libs/kappa-data-client \
		--additional-properties=packageName=kappa_data_client \
		--additional-properties=projectName=kappa-data-client \
		--additional-properties=packageVersion=0.0.0
	rm -f libs/**/*requirements.txt
	rm -f libs/**/setup.*

kappa-fn-code-client:
	wget localhost:8030/openapi.json -O openapi-kappa-fn-code.json
	rm -rf libs/kappa-fn-code-client
	docker run --rm \
		-v "$(PWD):/local" openapitools/openapi-generator-cli generate \
		-i /local/openapi-kappa-fn-code.json \
		-g python \
		-o /local/libs/kappa-fn-code-client \
		--additional-properties=packageName=kappa_fn_code_client \
		--additional-properties=projectName=kappa-fn-code-client \
		--additional-properties=packageVersion=0.0.0
	rm -f libs/**/*requirements.txt
	rm -f libs/**/setup.*

kappa-fn-logs-client:
	wget localhost:8040/openapi.json -O openapi-kappa-fn-logs.json
	rm -rf libs/kappa-fn-logs-client
	docker run --rm \
		-v "$(PWD):/local" openapitools/openapi-generator-cli generate \
		-i /local/openapi-kappa-fn-logs.json \
		-g python \
		-o /local/libs/kappa-fn-logs-client \
		--additional-properties=packageName=kappa_fn_logs_client \
		--additional-properties=projectName=kappa-fn-logs-client \
		--additional-properties=packageVersion=0.0.0
	rm -f libs/**/*requirements.txt
	rm -f libs/**/setup.*

kappa-logs-client:
	wget localhost:8050/openapi.json -O openapi-kappa-logs.json
	rm -rf libs/kappa-logs-client
	docker run --rm \
		-v "$(PWD):/local" openapitools/openapi-generator-cli generate \
		-i /local/openapi-kappa-logs.json \
		-g python \
		-o /local/libs/kappa-logs-client \
		--additional-properties=packageName=kappa_logs_client \
		--additional-properties=projectName=kappa-logs-client \
		--additional-properties=packageVersion=0.0.0
	rm -f libs/**/*requirements.txt
	rm -f libs/**/setup.*

kappa-runner-client:
	wget localhost:8060/openapi.json -O openapi-kappa-runner.json
	rm -rf libs/kappa-runner-client
	docker run --rm \
		-v "$(PWD):/local" openapitools/openapi-generator-cli generate \
		-i /local/openapi-kappa-runner.json \
		-g python \
		-o /local/libs/kappa-runner-client \
		--additional-properties=packageName=kappa_runner_client \
		--additional-properties=projectName=kappa-runner-client \
		--additional-properties=packageVersion=0.0.0
	rm -f libs/**/*requirements.txt
	rm -f libs/**/setup.*

clients: kappa-client kappa-data-client kappa-fn-code-client kappa-fn-logs-client kappa-logs-client kappa-runner-client
