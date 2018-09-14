import java.io.File;
import java.io.IOException;
import org.openslide.OpenSlide;
import org.openslide.AssociatedImage;

public class OpenslideTest {
	public static void main(String[] args) {
		String wsi = "/home/sakulaki/yolo-yuli/one_stop_test/tif_java/XB1800118.tif";
		try {
			OpenSlide slide = new OpenSlide(new File(wsi));
			int levelCount = slide.getLevelCount();
			System.out.println("levelCount: " + levelCount);
			slide.close();
		} catch (Exception e) {
			System.err.println(e);
		}
		System.out.println("done.");
	}
}
