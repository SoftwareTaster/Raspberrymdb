require "id3tag"
out_path = "C:\\Users\\lenovo\\Desktop\\files\\show_mp3\\"
out_path = "F:\\source\\Raspberrymdb\\app\\static\\files\\cover\\"
ID3Tag.read(File.open(ARGV[0], "rb")) do |tag|
	pureName = ARGV[0].split("\\")[-1].split(".")[0] #更换操作系统时要修改这句
	frameAPIC = tag.get_frame(:APIC)
    if frameAPIC
	    image = frameAPIC.content
	    coverName = pureName + ".png"
	    open(out_path+coverName,"wb") do |cover|
	    	cover.write(image)
	    end
	end
end
