# color-blind friendly palettes
cbbPalette <- 
  c("#000000", "#E69F00", "#56B4E9", 
    "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

cbPalette <-
  c("#999999", "#E69F00", "#56B4E9", 
    "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

# legend options

# large, bold lettering with legend at bottom (standard)
large.bold.bottom.legend <- 
  theme(legend.position = 'bottom',
        legend.text = element_text(face = 'bold', size = 16),
        legend.title = element_blank(),
        axis.text.x = element_text(size = 12, face = 'bold'),
        axis.text.y = element_text(size = 12, face = 'bold'),
        axis.ticks = element_blank(),
        axis.title.x = element_text(size = 16, face = 'bold'),
        axis.title.y = element_text(size = 16, face = 'bold'),
        plot.title = element_text(size = 20, face = 'bold'))

# large, bold lettering with legend at bottom with large facets
large.bold.bottom.legend.facet <- 
  theme(legend.position = 'bottom',
        strip.text.y = element_text(size = 15, angle = 0, face = 'bold'),
        strip.text.x = element_text(size = 15, angle = 0, face = 'bold'),
        strip.background = element_rect(fill = 'white',
                                        colour = 'black', size = 1),
        legend.text = element_text(face = 'bold', size = 16),
        legend.title = element_blank(),
        axis.text.x = element_text(size = 12, face = 'bold'),
        axis.text.y = element_text(size = 12, face = 'bold'),
        axis.ticks = element_blank(),
        axis.title.x = element_text(size = 16, face = 'bold'),
        axis.title.y = element_text(size = 16, face = 'bold'),
        plot.title = element_text(size = 20, face = 'bold'))
