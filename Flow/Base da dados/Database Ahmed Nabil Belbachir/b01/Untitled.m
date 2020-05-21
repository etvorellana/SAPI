img = imread('07180001.jpg');
%imshow(img);
YIQ = uint8(zeros(size(img)));
for i=1:size(img,1)
    for j=1:size(img,2)
        YIQ(i,j,1)=0.2989*img(i,j,1)+0.5870*img(i,j,2)+0.1140*img(i,j,3);
        YIQ(i,j,2)=0.596*img(i,j,1)-0.274*img(i,j,2)-0.322*img(i,j,3);
        YIQ(i,j,3)=0.211*img(i,j,1)-0.523*img(i,j,2)+0.312*img(i,j,3);
    end
end

imshow(YIQ);
%subplot(1,2,1); imshow(img);title('Imagem original');
%subplot(1,2,2); imshow(YIQ);title('YIQ');