
def response_T_Plus_dt(dempingsfactor: float, massa: float, veerconstante: float, acceleratie_frame_t: float, response_t: float, response_t_min_dt, dt):
    """
    parameters:
    dempingsfactor: float, de dempingsfactor gamma is de denpingsfactor van het massaveersysteem.
    massa: float, De de massa van de massa
    veerconstante: float, het collectieve veerconstante van alle veren in het massa veersysteem
    float, acceleratie_frame_t, de versnelling van het frame op een gegeven tijd t
    response_t: float, de response of relatieve positie van de massa ten opzichten van het frame op een gegeven tijd t
    response_t_min_dt: float, de response of relatieve positie van de massa ten opzichten van het frame op een gegeven tijd t - h
    dt: float, Het verschil in tijdsmomenten.
    """
    response_t_plus_dt = (
                          response_t            * ( (dempingsfactor*dt/massa) + ((dt**2)*veerconstante/massa) + 2)
                        + response_t_min_dt     * ( 1 - (dempingsfactor*dt/massa) ) 
                        + acceleratie_frame_t   * ( (dt**2)*massa )
                        )
    return response_t_plus_dt

