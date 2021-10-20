# PVMPATCH: Towards Bug Detection, Rectification and Evolution in Python Virtual Machines



## Structure

- **code**    [README there]() has details for reproducing data.
  - **util**  Components of PVMPATCH
  - **tool**  other tool
- **config**  configuration file
  - **configure.json**：Configure the information of the project to be fixed. 
  - **patch_template.json**: patch template list
- **corpus**  Python source code
- **output**  The repaired code and its repair report
- **statistics**  Charts used in the paper



## Environment

You need at least the following dependencies:

- **Infer**

  Our tecnique is built on top of the open source *Infer* static analyzer, you can follow the [Infdoc](https://github.com/facebook/infer/releases/tag/v1.1.0) to install *Infer v1.1.0*. Maybe other versions are also available, but we recommend this version

- **Python**

  The version of Python we used is *3.9.5*. Maybe other versions are also available, we recommend that your python version is as high as 3.7 or above. 

  



## How to use

#### Fully automatic process

The configuration file `./config/configure.json` is important. The information of a single project corpus in the configuration file is as follows：

```
{
      "project_name": "cpython-3.10",
      "download_url": "https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz" ,
      "md5": "729e36388ae9a832b01cf9138921b383",
      "project_path": "../corpus/cpython-3.10/Python-3.10.0"
    }
```

You can change various configurations in this file. Then run the following commands in `./code` . 

```
./python3 main.py
```

It will automatically complete the download, preprocessing, vulnerability analysis, repair, and verification of the specified project to be repaired, and output the repaired project and its corresponding detection and repair reports. 

For other more detailed usage methods, see [README there]() 









 













