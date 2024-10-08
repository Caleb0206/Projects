import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/**
 * Contains file processing behavior for the project.
 * You will modify only the following methods:
 * - parseLineUsingLittleNumber()
 * - parseLineUsingBigNumber()
 * You do not need to run this class directly.
 *
 * @author Vanessa Rivera
 * @author Caleb Huang
 */
public class FileProcessor {
    /**
     * Automatically called multiple times when parsing an input text file, once for each line.
     * The included tests control whether the LittleNumber or BigNumber version is used.
     *
     * @param line The line from the input file, including any newline characters
     */
    public static void parseLineUsingLittleNumber(String line) {
        LittleNumber a;
        LittleNumber b;
        String [] separated = line.split("\\s+"); // the "\\s+" causes ALL the whitespace to be eliminated

        if (separated.length != 3) {
            return;
        }
        if (!(separated[1].equals("+") || separated[1].equals("*") || separated[1].equals("^") )) {
            return ;
        }

        a = LittleNumber.fromString(separated[0]);
        b = LittleNumber.fromString(separated[2]);

        LittleNumber result;
        switch(separated[1]) {
            case "+":
                result = a.add(b);
                System.out.println(a + " + " + b + " = " + result.toString());
                break;
            case "*":
                result = a.multiply(b);
                System.out.println(a + " * " + b + " = " + result.toString());
                break;
            case "^":
                result = a.exponentiate(Integer.parseInt(b.toString()));
                System.out.println(a + " ^ " + b + " = " + result.toString());
                break;

        }

    }

    /**
     * Automatically called multiple times when parsing an input text file, once for each line.
     * The included tests control whether the LittleNumber or BigNumber version is used.
     *
     * @param line The line from the input file, including any newline characters
     */
    public static void parseLineUsingBigNumber(String line) {
        BigNumber a;
        BigNumber b;
        String [] separated = line.split("\\s+");

        if (separated.length != 3) {
            return;
        }
        if (!(separated[1].equals("+") || separated[1].equals("*") || separated[1].equals("^") )) {
            return ;
        }
        a = BigNumber.fromString(separated[0]);
        b = BigNumber.fromString(separated[2]);

        BigNumber result;
        switch(separated[1]) {
            case "+":
                result = a.add(b);
                System.out.println(a + " + " + b + " = " + result.toString());
                break;
            case "*":
                result = a.multiply(b);
                System.out.println(a + " * " + b + " = " + result.toString());
                break;
            case "^":
                result = a.exponentiate(Integer.parseInt(b.toString()));
                System.out.println(a + " ^ " + b + " = " + result.toString());
                break;
        }
    }

    /**
     * Called by the included test file. You do not need to run this method directly.
     * <strong>Do not</strong> modify this method.
     *
     * @param args Command-line arguments
     *             0: The input file path. (Required)
     *             1: Option to use "little" or "big" number parsing. (Required)
     */
    public static void main(String[] args) {
        try (BufferedReader reader = new BufferedReader(new FileReader(args[0]))) {
            String line;
            while ((line = reader.readLine()) != null) {
                switch (args[1]) {
                    case "little":
                        parseLineUsingLittleNumber(line);
                        break;
                    case "big":
                        parseLineUsingBigNumber(line);
                        break;
                    default:
                        throw new IllegalArgumentException();
                }
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.printf("Expected 2 command-line arguments, got %d.%n", args.length);
        } catch (IOException e) {
            System.out.printf("Failed to read file %s.%n", args[0]);
        } catch (IllegalArgumentException e) {
            System.out.printf("Option %s is invalid, must be 'little' or 'big'.%n", args[1]);
        }
    }
}
