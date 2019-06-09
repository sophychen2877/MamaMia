import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.*;

public class LanguageModel {
	public static class Map extends Mapper<LongWritable, Text, Text, Text> {

		int threashold;

		@Override
		public void setup(Context context) {
			Configuration conf = context.getConfiguration();
			threashold = conf.getInt("threashold",20);
			// how to get the threashold parameter from the configuration?
		}


		@Override
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			if((value == null) || (value.toString().trim()).length() == 0) {
				return;
			}
			//this is cool\t20
			String line = value.toString().trim();

			String[] wordsPlusCount = line.split("\t");
			if(wordsPlusCount.length < 2) {
				return;
			}

			String[] words = wordsPlusCount[0].split("\\s+");
			int count = Integer.valueOf(wordsPlusCount[1]);
			int wordsLen = words.length;

			//how to filter the n-gram lower than threashold
			if (count<threashold){return;}
			if (wordsLen<=1){return;}
			//this is --> cool = 20

			//what is the outputkey?
			StringBuilder sb = new StringBuilder();
			StringBuilder outputValue = new StringBuilder();
			for (int i=0; i<wordsLen-1;i++){
				sb.append(words[i]);
				sb.append(" ");
			}
			outputValue = words[wordsLen-1].append(" = ").append(count);
			context.write(new Text(sb.toString().trim()),new Text(outputValue.toString()));




			//what is the outputvalue?

			//write key-value to reducer?
		}
	}

	public static class Reduce extends Reducer<Text, Text, DBOutputWritable, NullWritable> {

		int n;
		// get the n parameter from the configuration
		@Override
		public void setup(Context context) {
			Configuration conf = context.getConfiguration();
			n = conf.getInt("n", 5);
		}


		@Override
		public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {

			//because we wanna introduce an ordered (based on the occurence)keyvalue pair, we will use TreeMap(not hashmap)and introduce reversorder collections
			TreeMap<Integer, ArrayList<String>> countMap = new TreeMap<Integer,ArrayList<String>>(Collections.reverseOrder());

		//iterete through the values Text iterator
			for (Text value: values){
				String s = value.toString().trim();
				String followingWord = s.split("=")[0].trim();
				int occur = Integer.parseInt(s.split("=")[1].trim());

				if (countMap.containsKey(occur)){
					countMap.get(occur).add(followingWord);
				}else{
					ArrayList<String> list = new ArrayList<String>();
					list.add(followingWord);
					countMap.put(occur,list);
				}
			}
		//now a treemap with reversrOrder of key is created, for it might look like ->	{10:[big,bird], 5:[as],3:[big]}
		//iterate through the keysets for the given number of topN which will be write database as DBOutputwritable(String String int)
			Iterator<Integer> iter = countMap.keySet().iterator();
			for (int i=0;i<n&&iter.hasNext();i++){
				int count = iter.next();
				List<String>words=countMap.get(count);
				for(String word:words){
					context.write(new DBOutputWritable(key.toString(),word, count),NullWritable.get());//context output is always the keyvalue pair
			}
		}



			//can you use priorityQueue to rank topN n-gram, then write out to hdfs?
		}
	}
}
