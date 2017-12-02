// package com.google.cloud.dataflow.examples;
package com.example;

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

public class MinimalWordCount {

  public static void main(String[] args) {
    DataflowPipelineOptions options = PipelineOptionsFactory.create()
    .as(DataflowPipelineOptions.class);
    options.setRunner(BlockingDataflowPipelineRunner.class);
    options.setProject("windy-watch-186102");
    // The 'gs' URI means that this is a Google Cloud Storage path
    options.setStagingLocation("gs://duplicates/staging");

    Pipeline p = Pipeline.create(options);

    // TODO: Get txt file
    p.apply(TextIO.Read.from("gs://duplicates/question-id.csv"))
      // .apply(ParDo.named("ExtractWords").of(new DoFn<String, String>() {
      //   @Override
      //   public void processElement(ProcessContext c) {
      //     for (String word : c.element().split("[^a-zA-Z']+")) {
      //       if (!word.isEmpty()) {
      //         c.output(word);
      //       }
      //     }
      //   }
      // }))
      .apply(GroupByKey.<String, String>create())
      // .apply(Count.<String>perElement())

      .apply(MapElements.via(


        new SimpleFunction<KV<String, Iterable<String>>, String>() {
        @Override
        public String apply(KV<String, Iterable<String>> element) {
          return element.getKey() + "," + element.getValue();
        }

      }))
      .apply(TextIO.Write.to("gs://duplicates/duplicates.csv"));

    p.run();
  }

}
