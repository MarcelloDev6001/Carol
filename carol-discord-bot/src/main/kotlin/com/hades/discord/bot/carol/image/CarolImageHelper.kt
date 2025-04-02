package com.hades.discord.bot.carol.image

import jdk.incubator.vector.Vector
import okhttp3.OkHttpClient
import okhttp3.Request
import java.awt.Graphics2D
import java.awt.RenderingHints
import java.awt.image.BufferedImage
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.InputStream
import javax.imageio.ImageIO

object CarolImageHelper {
    fun loadImage(localImagePath: String): BufferedImage {
        val inputStream: InputStream? = this::class.java.classLoader.getResourceAsStream("images/${localImagePath}")
        return ImageIO.read(inputStream)
    }

    fun loadImageFromWeb(url: String): BufferedImage {
        val client = OkHttpClient()
        val request = Request.Builder().url(url).build()
        val response = client.newCall(request).execute()
        val webImage: BufferedImage = ImageIO.read(response.body?.byteStream())
        return webImage
    }

    fun resizeImage(image: BufferedImage, width: Int, height: Int): BufferedImage {
        val resizedImage = BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB)
        val g2d = resizedImage.createGraphics()
        g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR)
        g2d.drawImage(image, 0, 0, width, height, null)
        g2d.dispose()
        return resizedImage
    }

    fun combineImages(img1: BufferedImage, img2: BufferedImage, img2Position: Array<Int>): BufferedImage {
        val combinedImage = BufferedImage(img1.width, img1.height, BufferedImage.TYPE_INT_ARGB)
        val g: Graphics2D = combinedImage.createGraphics()
        g.drawImage(img1, 0, 0, null)
        g.drawImage(img2, img2Position[0], img2Position[1], null)
        g.dispose()

        return combinedImage
    }

    fun convertToByteArray(img: BufferedImage): ByteArray
    {
        val outputStream = ByteArrayOutputStream()
        ImageIO.write(img, "png", outputStream)
        return outputStream.toByteArray()
    }
}