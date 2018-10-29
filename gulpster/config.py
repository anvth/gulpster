import yaml


def read_config_file():
	with open('/Users/anvith.shivakumara/Workspace/artkradle/gulpster/gulpster/config.yaml') as file_name:
		config_data = yaml.load(file_name)

	return config_data['rabbitmq']