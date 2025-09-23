// 计算最高分
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("请输入学生人数：");
        int n = scanner.nextInt();
        int[] scores = new int[n];
        System.out.println("请输入每位学生的分数：");
        for (int i = 0; i < n; i++) {
            scores[i] = scanner.nextInt();
        }
        int maxScore = findMaxScore(scores);
        System.out.println("最高分是：" + maxScore);
        scanner.close();
    }

    public static int findMaxScore(int[] scores) {
        int max = scores[0];
        for (int i = 1; i < scores.length; i++) {
            if (scores[i] > max) {
                max = scores[i];
            }
        }
        return max;
    }
}





