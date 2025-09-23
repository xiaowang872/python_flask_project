// 计算邮费
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int weight = input.nextInt();
        int c = input.next().charAt(0); // 加急服务标记
        int cost = 8;
        if (weight > 1000) {
            weight -= 1000;
            cost += 4 * (int)Math.ceil(weight / 500.0);

        }
        if (c == 'y') {
            cost += 5;
            
        }

        System.out.println(cost);
    }
}


