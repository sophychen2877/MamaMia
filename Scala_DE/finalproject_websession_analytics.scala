// use docker zeppelin
//docker run -it --rm -p 8888:8080 -v /Users/de_programming/data/:/data apache/zeppelin:0.8.1

import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.types.{StructType, StructField, StringType, IntegerType,DoubleType,TimestampType}
import org.apache.spark.sql.Row

val sqlContext = new SQLContext(sc)
val customSchema = StructType(Array(
   StructField("timestamptimestamp", TimestampType, true),
   StructField("elb", StringType, true),
   StructField("client:port", StringType, true),
   StructField("backend:port", StringType, true),
   StructField("request_processing_time", DoubleType, true),
   StructField("backend_processing_time", DoubleType, true),
   StructField("response_processing_time", DoubleType, true),
   StructField("elb_status_code", IntegerType, true),
   StructField("backend_status_code", IntegerType, true),
   StructField("received_bytes", IntegerType, true),
   StructField("sent_bytes", IntegerType, true),
   StructField("request", StringType, true),
   StructField("user_agent", StringType, true),
   StructField("ssl_cipher", StringType, true),
   StructField("ssl_protocol", StringType, true))
)
val df = sqlContext.read
    .format("com.databricks.spark.csv")
    .option("delimiter"," ")
    .option("header","true")
    .schema(customSchema) 
    .load(file)


val file = "/data/sample_web.log"
val step1 = df.select("timestamp", "backend:port", "request").withColumn("epoch", $"timestamp".cast("Long"))
.withColumn("backend", split($"backend:port", ":")(0)).drop("backend:port").sample(0.05)
// first step =  massage the data in a way that contains all the information that we need, massage the backend column, cast the timestamp from string to epoch timestamp, sub sampling the data (5%)

val step2 = step1.withColumn("collected", collect_list(struct("*"))
.over(Window.partitionBy(col("backend")).orderBy("epoch"))).groupBy("backend").agg(max("collected"))
// step2 start gathering the data to the collected column and give us an view so that we can pick the max which collect all the necessary data points(partition by backend column and order by epoch timestamp)
