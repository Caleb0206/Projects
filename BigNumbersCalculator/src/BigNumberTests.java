import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
/**
 * An empty class for unit tests of your new classes.
 * @author calebhuang
 */
public class BigNumberTests {
    @Test
    public void testBigNumber1() {
        BigNumber a = new BigNumber();
        a = BigNumber.fromString("12345");
        Assertions.assertEquals("12345", a.toString());
        BigNumber empty = new BigNumber();
        Assertions.assertEquals("", empty.toString());
        Assertions.assertEquals("", BigNumber.fromString("").toString());
    }

    @Test
    public void testAddSimple() {
        BigNumber a = new BigNumber();
        a = BigNumber.fromString("1");
        Assertions.assertEquals("3", a.add(BigNumber.fromString("2")).toString());
    }
    @Test
    public void testAddCarry() {
        BigNumber c = new BigNumber();
        c = BigNumber.fromString("1");
        BigNumber d = new BigNumber();
        Assertions.assertEquals("100", c.add(BigNumber.fromString("99")).toString());
        d = BigNumber.fromString("99");
        Assertions.assertEquals("100", d.add(c).toString());

        BigNumber e = new BigNumber();
        e = BigNumber.fromString("15");
        BigNumber f = new BigNumber();
        f = BigNumber.fromString("16");
        Assertions.assertEquals("31", e.add(f).toString());
        Assertions.assertEquals("24", e.add( BigNumber.fromString("9")).toString());
        Assertions.assertEquals("16", e.add(c).toString());


    }

    @Test
    public void testMultiplySimple() {
        BigNumber a = new BigNumber();
        a = BigNumber.fromString("2");
        BigNumber b = new BigNumber();
        b = BigNumber.fromString("3");
        Assertions.assertEquals("6", a.multiply(b).toString());

        a = BigNumber.fromString("12");
        b = BigNumber.fromString("13");
        Assertions.assertEquals("156", a.multiply(b).toString());
    }
    @Test
    public void testMultiplyCarry() {
        BigNumber a = new BigNumber();
        a = BigNumber.fromString("4");
        BigNumber b = new BigNumber();
        b = BigNumber.fromString("16");
        Assertions.assertEquals("64", a.multiply(b).toString());

        a = BigNumber.fromString("22");
        b = BigNumber.fromString("33");
        Assertions.assertEquals("726", a.multiply(b).toString());
    }

    @Test
    public void testExp() {
        BigNumber a = new BigNumber();
        a = BigNumber.fromString("2");

        Assertions.assertEquals("16", a.exponentiate(4).toString());
        Assertions.assertEquals("32", a.exponentiate(5).toString());
        Assertions.assertEquals("1048576", a.exponentiate(20).toString());


        BigNumber b = new BigNumber();
        b = BigNumber.fromString("12");
        Assertions.assertEquals("144", b.exponentiate(2).toString());

        Assertions.assertEquals("1", b.exponentiate(0).toString());

    }
    @Test
    public void testFromFileProcessorTest() {
        BigNumber a = new BigNumber();
        a = BigNumber.fromString("5");
        System.out.println(a.exponentiate(6));
        Assertions.assertEquals("15625", a.exponentiate(6).toString());

        a = BigNumber.fromString("10");
        BigNumber b = new BigNumber();
        b = BigNumber.fromString("9999999999");
        Assertions.assertEquals("99999999990", a.multiply(b).toString());

    }
}
