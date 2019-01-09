package bsu.fpmi

import java.io.{File, PrintWriter}

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object PageRank {
  def main(args: Array[String]) {
    val sc = new SparkContext(new SparkConf().setAppName("Task3"))

    val file = sc.textFile("hdfs://localhost:8020" + args(0))

    val links = file.map{ line =>
      val tokens = line.split("\\s")
      (tokens(0).toLong, (tokens(1).toLong, tokens(2).toDouble))
    }

    val outgoingWeightSums = links.mapValues(_._2)
      .reduceByKey(_ + _)

    val C = 0.85
    val transitionMatrix = links.join(outgoingWeightSums)
      .mapValues { case ((j, w), sum_w) => (j, C * w / sum_w) }
      .cache()

    val vertices = links.flatMap{ case (i, (j, w)) => Array(i, j) }.distinct()
    val n = vertices.count().toInt
    val v = vertices.map(vertex => (vertex, 1.0/n))
    var ranks = vertices.map(vertex => (vertex, 1.0))

    val iterations = 50
    val errors = new Array[Double](iterations)

    for (iter <- 0 until iterations) {
      var newRanks = ranks.join(transitionMatrix)
        .values
        .map { case (rank, (j, w)) => (j, w * rank) }
        .reduceByKey(_ + _)

      val gamma = ranks.values.map(Math.abs).sum() - newRanks.values.map(Math.abs).sum()
      newRanks = newRanks.rightOuterJoin(v)
        .map { case (i, (rank, value)) => (i, rank.getOrElse(0.0) + gamma * value) }

      errors(iter) = newRanks.join(ranks)
        .values
        .map { case (v1, v2) => Math.abs(v1 - v2) }
        .sum() / n

      ranks = newRanks
    }

    val pw = new PrintWriter(new File("errors.txt"))
    for (i <- errors.indices) {
      pw.println(s"$i\t${errors(i)}")
    }
    pw.close()

    val topCount = 50
    val topRanks = ranks.takeOrdered(topCount)(Ordering[Double].reverse.on(_._2))
      .map { case (i, rank) => s"$i\t$rank" }

    val resultsPw = new PrintWriter(new File(args(1)))
    topRanks.foreach(resultsPw.println)
    resultsPw.close()
  }
}
