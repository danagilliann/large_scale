// package com.google.cloud.dataflow.examples;
package com.example;

import java.lang.String;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

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

public class MinimalWordCount {

  private static final Logger LOG = LoggerFactory.getLogger(MinimalWordCount.class);

  public static void main(String[] args) {
    DataflowPipelineOptions options = PipelineOptionsFactory.create()
    .as(DataflowPipelineOptions.class);
    options.setRunner(BlockingDataflowPipelineRunner.class);
    options.setProject("windy-watch-186102");
    // The 'gs' URI means that this is a Google Cloud Storage path
    options.setStagingLocation("gs://duplicates/staging");


    Pipeline p = Pipeline.create(options);
    final Map<String, ArrayList<String>> mapQuestionId = new HashMap<>();

    p.apply(TextIO.Read.from("gs://duplicates/question-id.txt"))
     // Concept #2: Apply a ParDo transform to our PCollection of text lines. This ParDo invokes a
     // DoFn (defined in-line) on each element that tokenizes the text line into individual words.
     // The ParDo returns a PCollection<String>, where each element is an individual word in
     // Shakespeare's collected texts.
     .apply(ParDo.named("ExtractWords").of(new DoFn<String, String>() {
       @Override
       public void processElement(ProcessContext c) {
         String[] questionId = c.element().split(",");
         // System.out.println(questionId);

         // for (int i = 0; i < questionId.length; ++i) {
         //   LOG.info("questionId " + questionId[i]);
         // }

         LOG.info("questionId[0] " + questionId[0]);
         final ArrayList<String> idList = mapQuestionId.get(questionId[0]);

         if (idList == null) {
           ArrayList<String> newIdsList = new ArrayList();
           newIdsList.add(questionId[1]);
           mapQuestionId.put(questionId[0], newIdsList);

           LOG.info("MISS: questionIds: " + mapQuestionId.get(questionId[0]));
         } else {
           idList.add(questionId[1]);
           mapQuestionId.put(questionId[0], idList);

           LOG.info("HIT: questionIds: " + mapQuestionId.get(questionId[0]));
         }

         LOG.info("mapQuestionId: " + mapQuestionId.toString());

         for (String word : questionId) {
           if (!word.contains("qId")) {
             c.output(word);
           }
         }
       }
     }))
     // Concept #3: Apply the Count transform to our PCollection of individual words. The Count
     // transform returns a new PCollection of key/value pairs, where each key represents a unique
     // word in the text. The associated value is the occurrence count for that word.
     .apply(Count.<String>perElement())
     // .apply(GroupByKey.create())

     // Apply a MapElements transform that formats our PCollection of word counts into a printable
     // string, suitable for writing to an output file.
     .apply("FormatResults", MapElements.via(new SimpleFunction<KV<String, Long>, String>() {
       @Override
       public String apply(KV<String, Long> input) {
         String question = input.getKey();
         ArrayList<String> questionIds = mapQuestionId.get(question);
         // StringBuiler questionIds = new StringBuilder();
         // String questionIds = String.join(",", mapQuestionId.get(question));

         return question + "," + questionIds;
       }
     }))
     // Concept #4: Apply a write transform, TextIO.Write, at the end of the pipeline.
     // TextIO.Write writes the contents of a PCollection (in this case, our PCollection of
     // formatted strings) to a series of text files in Google Cloud Storage.
     // CHANGE 3/3: The Google Cloud Storage path is required for outputting the results to.
     .apply(TextIO.Write.to("gs://duplicates/outputs"));

    // Run the pipeline.
    p.run();
  }
}
