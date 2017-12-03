// package com.google.cloud.dataflow.examples;
package com.example;

import java.lang.String;
import java.lang.StringBuilder;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.stream.StreamSupport;
import java.util.stream.Collectors;

import com.google.cloud.dataflow.sdk.Pipeline;
import com.google.cloud.dataflow.sdk.io.TextIO;
import com.google.cloud.dataflow.sdk.options.DataflowPipelineOptions;
import com.google.cloud.dataflow.sdk.options.PipelineOptionsFactory;
import com.google.cloud.dataflow.sdk.runners.BlockingDataflowPipelineRunner;
import com.google.cloud.dataflow.sdk.transforms.Count;
import com.google.cloud.dataflow.sdk.transforms.DoFn;
import com.google.cloud.dataflow.sdk.transforms.GroupByKey;
import com.google.cloud.dataflow.sdk.transforms.MapElements;
import com.google.cloud.dataflow.sdk.transforms.ParDo;
import com.google.cloud.dataflow.sdk.transforms.SimpleFunction;
import com.google.cloud.dataflow.sdk.values.KV;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Duplicates {

  private static final Logger LOG = LoggerFactory.getLogger(Duplicates.class);

  public static void main(String[] args) {
    DataflowPipelineOptions options = PipelineOptionsFactory.create()
    .as(DataflowPipelineOptions.class);
    options.setRunner(BlockingDataflowPipelineRunner.class);
    options.setProject("windy-watch-186102");
    options.setStagingLocation("gs://duplicates/staging");


    Pipeline p = Pipeline.create(options);
    final Map<String, ArrayList<String>> mapQuestionId = new HashMap<>();

    p.apply(TextIO.Read.from("gs://duplicates/question-id.csv"))
     .apply(ParDo.named("ExtractWords").of(new DoFn<String, KV<String, String>>() {
       @Override
       public void processElement(ProcessContext c) {
         String[] questionIdPairArray = c.element().split(",");

         KV<String, String> questionIdPair = KV.of(questionIdPairArray[0], questionIdPairArray[1]);
         c.output(questionIdPair);
       }
     }))
     .apply(GroupByKey.<String, String>create())
     .apply("FormatResults", MapElements.via(new SimpleFunction<KV<String, Iterable<String>>, String>() {
       @Override
       public String apply(KV<String, Iterable<String>> input) {
         StringBuilder questionIds = new StringBuilder();
         String separator = "";

         for (String string : input.getValue()) {
           questionIds.append(separator);
           questionIds.append(string);
           separator = ",";
         }

         return input.getKey() + "," + questionIds;
       }
     }))
     .apply(TextIO.Write.to("gs://duplicates/outputs/duplicates")
                        .withoutSharding()
                        .withSuffix(".csv"));

    p.run();
  }
}
