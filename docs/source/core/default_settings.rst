Default Settings
================

Customize data_importer decoders

**DATA_IMPORTER_EXCEL_DECODER**
 Default value is cp1252

**DATA_IMPORTER_DECODER**
 Default value is UTF-8

**DATA_IMPORTER_TASK**
 Need Celery installed to set importers as Task
  `default value is False`

**DATA_IMPORTER_QUEUE**
 Set Celery Queue in DataImpoter Tasks
  `default value is DataImporter`

**DATA_IMPORTER_TASK_LOCK_EXPIRE**
 Set task expires time
  `default value is 60 * 20`
