# devopsblog
For installing platform perform:
`. ./install.sh <USERNAME> <ENVIRONMENT> <VIRTUAL ENV NAME>` in the root of git project directory
After that you can access your venv account just with alias `<VIRTUAL ENV NAME>`

To see the list of available commands type `fab help` or see the list below:
## List of available functions
- `fab core.apply_tf:<USERNAME>,<ENVIRONMENT>,<PROFILE>` - applies terraform states from terraform/profiles/<PROFILE> directory
- `fab core.destroy_tf:<USERNAME>,<ENVIRONMENT>,<PROFILE>` - destroys terraform states from terraform/profiles/<PROFILE> directory
- `fab core.install_terraform` - installs terraform via wget from zip archive. You can specify download URL in global.yaml config file
- `fab core.init_terraform_profiles:<USERNAME>,<ENVIRONMENT>` - initializes terraform backend for all profiles. s3:// bucket for states and profiles can be specified in global.yaml config file
- `fab core.init_bucket` - creates s3:// bucket for states. You can specify it in global.yaml config file 
- `fab core.configure_aws_credentials` - configures your aws credentials. You can set profile name in global.yaml config file
- `fab core.update_terraform:<USERNAME>,<ENVIRONMENT>` - updates and initializes terraform using `core.install_terraform` and `core.init_terraform_profiles` tasks. You can specify download URL, s3:// bucket for states and profiles in global.yaml config file
