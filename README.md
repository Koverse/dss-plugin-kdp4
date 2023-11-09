# dss-plugin-kdp4

## Connector for Dataiku DSS to connect with the Koverse Data Platform (KDP4)

### Prerequisite
Requires an installation of Dataiku - Data Science Studio (DSS)  
Installation instructions for mac: https://www.dataiku.com/product/get-started/mac/

### Installation

The plugin can be installed from the plugin page in Dataiku DSS:

![fetch_from_git_repository](resources/fetch_from_git_repository.png)

**Repository URL** (use either of)

- git@github.com:Koverse/dss-plugin-kdp4.git
- https://github.com/Koverse/dss-plugin-kdp4.git


![add_plugin_from_git_repo](resources/add_plugin_from_git_repo.png)

Next step is to create a code environment for the plugin (which installs needed dependencies:
                                                          kdp-python-connector with included kdp-api-python-client)
![add_code_environment](resources/add_code_environment.png)


After installation of the plugin, The 'Koverse KDP' plugin will be accessible from the DATASET menu of the Flow
in dataiku DSS.
Example:

![koverse_kdp_plugin_on_flow_page](resources/koverse_kdp_plugin_on_flow_page.png)

### Create Dataiku Preset

Under the **Settings** tab, create a preset for **API configuration**

![plugin_settings](resources/plugin_settings.png)

There are two supported authentication methods, **basic_login** and **json web token**. KDP plugin will use the method you choose for **Authentication method** when connecting to KDP.

#### Basic Login

![preset_basic_login](resources/preset_basic_login.png)

#### KDP JSON Web Token

![preset_jwt](resources/preset_jwt.png)


### Read/Write data from Dataiku DSS to KDP

Select the 'Koverse KDP Dataset' which is a dataiku custom dataset for reading and writing data to KDP.

![select_import_dataset](resources/select_dataset.png)

Provide required parameters and name for the dataset. When using an existing KDP dataset, the existing data can
be previewed:

![provide_export_dataset_parameters](resources/provide_export_dataset_parameters.png)

When using the dataset to create a new KDP4 dataset you can provide the dataset name. 
![creating_new_kdp4_dataset.png](resources/creating_new_kdp4_dataset.png)

After creation of the new dataset, you can select 'use_an_existing_dataset' and put in the dataset_id 
of the new KDP4 dataset to preview the data. 

![preview_dataset_data.png](resources/preview_dataset_data.png)


### For development: Creating new version of plugin

You can test changes outside DSS with the use_connector example (following the instructions contained in that example),
or add additional examples/tests in the same pattern. It will require the dependencies listed in requirements.txt
to be installed (code-env/python/spec/requirements.txt)

From kdp-dataiku-connector root... (may require sudo, or use of venv)

```pip install -r code-env/python/spec/requirements.txt```

Testing in Dataiku DSS can be done by importing the plugin as detailed in the steps above.
A feature branch can be targeted and imported. Also the plugin once installed can be converted
to a development plugin in DSS by selecting the menu option from ACTIONS as seen here...

![convert_to_dev_plugin](resources/convert_to_dev_plugin.png)

You can then edit in the DSS application, you will have to refresh any open DSS page after saving changes.  
DSS does have git integration, you can push changes out from DSS to the feature branch as you work with the plugin.  

Version should be manually updated in the plugin.json to the new minor version and also update the version in setup.py.
