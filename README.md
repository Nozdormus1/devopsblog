# devopsblog
For installing platform perform:
`. ./install.sh <USERNAME> <ENVIRONMENT> <VIRTUAL ENV NAME>` in the root of git project directory
After that you can access your venv account just with alias `<VIRTUAL ENV NAME>`

To see the list of available commands type `fab help` or see the list below:
## List of available functions
- `fab core.change_env:<USERNAME>,<ENVIRONMENT>` - changes environment for specified user
- `fab core.apply_tf:<USERNAME>,<PROFILE>` - applies terraform states from terraform/profiles/<PROFILE> directory
- `fab core.destroy_tf:<USERNAME>,<PROFILE>` - destroys terraform states from terraform/profiles/<PROFILE> directory
- `fab core.init_terraform_profiles:<USERNAME>` - creates s3:// bucket for states and initializes terraform backend for all profiles. s3:// bucket for states and profiles can be specified in global.yaml config file
- `fab core.configure_aws_credentials` - configures your aws credentials. You can set profile name in global.yaml config file
- `fab core.update_terraform:<USERNAME>` - updates and initializes terraform using `core.install_terraform` and `core.init_terraform_profiles` tasks. You can specify download URL, s3:// bucket for states and profiles in global.yaml config file
