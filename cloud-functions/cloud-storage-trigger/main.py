import functions_framework

from google.cloud import bigquery
@functions_framework.cloud_event

def upload_file(cloud_event):

    client = bigquery.Client()
    data = cloud_event.data
    file_name = data["name"]
    table_id = "{your-project-id}.udemy_course.us_states"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1
    )

    uri = "gs://cloud-func-trigger/"+file_name

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )

    load_job.result()
    destination_table = client.get_table(table_id)

    print(destination_table.num_rows)